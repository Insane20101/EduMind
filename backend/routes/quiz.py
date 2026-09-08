from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import time
import uuid
import asyncio

from utils.logger import get_logger
from rag.retriever import retrieve
from rag.generator import generate_with_retry
from rag.prompts import RAG_SYSTEM_PROMPT, QUIZ_INSTRUCTION
from rag.quiz_schema import QuizResponse
from database import db

quiz_router = APIRouter()
logger = get_logger(__name__)

class QuizGenerateRequest(BaseModel):
    unit_ids: List[str]
    difficulty: str
    count: int
    user_id: str = "test_user"

from routes.practice import get_subject_paths
from rag.chunker import chunk_markdown
import os

@quiz_router.post("/api/subjects/{subject_id}/quiz/generate")
async def generate_quiz(subject_id: str, req: QuizGenerateRequest):
    # 1. Native Qdrant Server-Side Payload Index Filtered Retrieval per Unit (KEYWORD Payload Index)
    chunks_per_unit = min(3, max(2, 12 // len(req.unit_ids))) if req.unit_ids else 3

    def fetch_unit_chunks(u_id):
        return retrieve(
            subject_id=subject_id,
            unit_id=u_id,
            query=f"Generate a {req.difficulty} difficulty multiple choice question about {u_id} syllabus concepts and problems",
            top_k=chunks_per_unit
        )

    all_retrieved_chunks = []
    if req.unit_ids:
        unit_tasks = [asyncio.to_thread(fetch_unit_chunks, uid) for uid in req.unit_ids]
        unit_results = await asyncio.gather(*unit_tasks, return_exceptions=True)
        for res in unit_results:
            if isinstance(res, list):
                # Strict exclusion of unassigned or non-selected unit chunks
                for c in res:
                    c_unit = c.get("metadata", {}).get("unit")
                    if c_unit and c_unit in req.unit_ids and c_unit != "unassigned":
                        all_retrieved_chunks.append(c)
        
    # 1B. Local Question Bank / Syllabus Markdown scoped strictly to requested units
    qb_path, _ = get_subject_paths(subject_id)
    if qb_path and os.path.exists(qb_path):
        try:
            with open(qb_path, 'r', encoding='utf-8') as f:
                qb_text = f.read()
            local_chunks = chunk_markdown(qb_text, os.path.basename(qb_path), subject_id, "unknown", "question_bank")
            for lc in local_chunks:
                chunk_unit = lc.get("metadata", {}).get("unit")
                if chunk_unit and chunk_unit in req.unit_ids and chunk_unit != "unassigned":
                    all_retrieved_chunks.append({
                        "chunk_id": f"qbank_{lc['metadata'].get('question_id', uuid.uuid4().hex[:8])}",
                        "similarity": 0.95,
                        "text": lc.get("text", ""),
                        "metadata": lc.get("metadata", {})
                    })
        except Exception as qb_err:
            logger.warning(f"Notice parsing local question bank for quiz: {qb_err}")

    # Deduplicate & cap to top-12 chunks for fast LLM generation
    seen_ids = set()
    unique_chunks = []
    for c in all_retrieved_chunks:
        if c["chunk_id"] not in seen_ids:
            seen_ids.add(c["chunk_id"])
            unique_chunks.append(c)
            if len(unique_chunks) >= 12:
                break
            
    required_chunks = req.count * 2
    retrieved_count = len(unique_chunks)
    
    logger.info("Quiz Generation initialized", extra={
        "subject_id": subject_id, 
        "unit_ids": req.unit_ids,
        "required_chunks": required_chunks,
        "retrieved_count": retrieved_count
    })
        
    # 3. Construct prompt with strict unit syllabus boundary instructions
    context_str = "\n\n".join([f"--- Chunk ID: {c['chunk_id']} ---\n{c['text']}" for c in unique_chunks])
    allowed_chunk_ids_str = "\n".join([f"- {c['chunk_id']}" for c in unique_chunks])
    
    system_prompt = RAG_SYSTEM_PROMPT.format(
        context=context_str,
        history="No prior conversation.",
        query=f"Generate {req.count} multiple-choice questions of {req.difficulty} difficulty covering EXCLUSIVELY the following selected unit(s): {', '.join(req.unit_ids)}."
    )
    
    unit_boundary_instruction = (
        f"\n\nSTRICT SYLLABUS & UNIT BOUNDARY INSTRUCTION:\n"
        f"Target Unit(s): {', '.join(req.unit_ids)}.\n"
        f"1. You MUST generate questions EXCLUSIVELY covering syllabus concepts, definitions, and topics belonging to: {', '.join(req.unit_ids)}.\n"
        f"2. Do NOT generate questions from any unselected units.\n"
        f"3. The 'unit' property of each generated question in the JSON response MUST be set to one of the exact strings: {', '.join(req.unit_ids)}."
    )
    
    citation_instruction = (
        f"\n\nCRITICAL CITATION RULE:\n"
        f"For every generated question, 'source_chunk_ids' MUST contain one or more of the EXACT literal Chunk ID strings listed below:\n"
        f"{allowed_chunk_ids_str}\n"
        f"Do NOT invent, alter, index, or summarize Chunk IDs. Use ONLY the exact literal strings provided above."
    )
    full_prompt = system_prompt + "\n" + QUIZ_INSTRUCTION + unit_boundary_instruction + citation_instruction
    
    # 4. Generation Loop with Validation and Retry
    def try_generate(error_msg=""):
        prompt_to_send = full_prompt
        if error_msg:
            prompt_to_send += f"\n\nYOUR PREVIOUS OUTPUT FAILED VALIDATION WITH ERROR:\n{error_msg}\nPLEASE FIX IT AND ENSURE IT MATCHES THE SCHEMA EXACTLY."
            
        raw_output = generate_with_retry(prompt_to_send, is_json=True, response_schema=QuizResponse)
        if not raw_output:
            return None, "API completely failed to return output."
            
        try:
            # Pydantic validation
            quiz_data = QuizResponse.model_validate_json(raw_output)
            return quiz_data, None
        except Exception as e:
            return None, str(e)

    quiz_data, error = try_generate()
    if error:
        logger.warning("Validation failed on first attempt, retrying", extra={"error": error})
        quiz_data, error2 = try_generate(error)
        if error2:
            logger.error("Validation failed on second attempt", extra={"error": error2})
            raise HTTPException(
                status_code=500,
                detail="Quiz generation failed due to formatting errors. Please try again."
            )
            
    # 5. Strict Guardrail Check: Exact-Set-Membership Verification
    def normalize_chunk_id(cid: str, valid_set: set) -> str:
        if not cid:
            return ""
        cid_clean = str(cid).strip().strip("'\"")
        if cid_clean in valid_set:
            return cid_clean
        return ""

    valid_questions = []
    valid_retrieved_set = {c["chunk_id"] for c in unique_chunks}
    
    for q in quiz_data.questions:
        valid_chunk_ids = []
        for cid in q.source_chunk_ids:
            norm_id = normalize_chunk_id(cid, valid_retrieved_set)
            if norm_id in valid_retrieved_set and norm_id not in valid_chunk_ids:
                valid_chunk_ids.append(norm_id)
                
        q.source_chunk_ids = valid_chunk_ids
        
        # STRICT GUARDRAIL: If retrieved chunks exist, discard ungrounded questions.
        # Otherwise, allow syllabus-level quiz generation with fallback grounding.
        if valid_retrieved_set:
            if not q.source_chunk_ids:
                logger.warning("DISCARDING UNGROUNDED QUESTION: No valid retrieved chunk IDs matched", extra={"question_text": q.question_text})
                continue
        else:
            if not q.source_chunk_ids:
                q.source_chunk_ids = [f"syllabus_{subject_id}"]
                
        # Verify the unit requested is valid
        if not q.unit or q.unit not in req.unit_ids:
            q.unit = req.unit_ids[0] if req.unit_ids else "Unit I"
            
        valid_questions.append(q)
            
    delivered_count = len(valid_questions)
    
    if delivered_count == 0:
        raise HTTPException(
            status_code=400,
            detail="Not enough course material retrieved for the selected unit(s) to generate a grounded quiz. Please select additional units or try again."
        )
    
    # 6. Storage
    quiz_doc = {
        "quiz_id": str(uuid.uuid4()),
        "user_id": req.user_id,
        "subject_id": subject_id,
        "timestamp": time.time(),
        "requested_count": req.count,
        "delivered_count": delivered_count,
        "difficulty": req.difficulty,
        "units": req.unit_ids,
        "questions": [q.model_dump() for q in valid_questions]
    }
    
    # Store using motor generic mock wrapper (await)
    await db.quizzes.insert_one(quiz_doc)
    quiz_doc.pop("_id", None)
    
    return {
        "requested_count": req.count,
        "delivered_count": delivered_count,
        "quiz": quiz_doc
    }

