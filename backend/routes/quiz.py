from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import time
import uuid

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

@quiz_router.post("/api/subjects/{subject_id}/quiz/generate")
async def generate_quiz(subject_id: str, req: QuizGenerateRequest):
    # 1. Retrieve chunks scoped to all requested units
    all_retrieved_chunks = []
    # If the user selects multiple units, we retrieve for each unit
    # to guarantee a mix.
    chunks_per_unit = max(4, (req.count * 2) // len(req.unit_ids) if req.unit_ids else req.count * 2)
    
    for unit_id in req.unit_ids:
        # Retrieve chunks specifically for this unit
        unit_chunks = retrieve(
            subject_id=subject_id,
            unit_id=unit_id,
            query=f"Generate a {req.difficulty} difficulty multiple choice question about {unit_id}",
            top_k=chunks_per_unit
        )
        all_retrieved_chunks.extend(unit_chunks)
        
    # Deduplicate chunks in case of overlap (though unlikely across units)
    seen_ids = set()
    unique_chunks = []
    for c in all_retrieved_chunks:
        if c["chunk_id"] not in seen_ids:
            seen_ids.add(c["chunk_id"])
            unique_chunks.append(c)
            
    # 2. Relaxed Context Rule (LLM will supplement missing context)
    required_chunks = req.count * 2
    retrieved_count = len(unique_chunks)
    
    logger.info("Quiz Generation initialized", extra={
        "subject_id": subject_id, 
        "unit_ids": req.unit_ids,
        "required_chunks": required_chunks,
        "retrieved_count": retrieved_count
    })
        
    # 3. Construct prompt
    context_str = "\n\n".join([f"--- Chunk ID: {c['chunk_id']} ---\n{c['text']}" for c in unique_chunks])
    
    system_prompt = RAG_SYSTEM_PROMPT.format(
        context=context_str,
        history="No prior conversation.",
        query=f"Generate {req.count} multiple-choice questions of {req.difficulty} difficulty covering the following units: {', '.join(req.unit_ids)}."
    )
    full_prompt = system_prompt + "\n" + QUIZ_INSTRUCTION
    
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
            
    # 5. Relaxed Constraint Check
    valid_questions = []
    retrieved_chunk_ids = {c["chunk_id"] for c in unique_chunks}
    
    for q in quiz_data.questions:
        valid_chunk_ids = []
        for cid in q.source_chunk_ids:
            if cid in retrieved_chunk_ids:
                valid_chunk_ids.append(cid)
            else:
                logger.warning("Filtering hallucinated chunk ID", extra={"chunk_id": cid, "subject_id": subject_id})
                
        q.source_chunk_ids = valid_chunk_ids
        
        # Filter out questions that have no valid grounding chunk IDs left
        if not q.source_chunk_ids:
            logger.warning("Filtering out entirely ungrounded question", extra={"question_text": q.question_text})
            continue
                
        # Verify the unit requested is valid
        if q.unit not in req.unit_ids:
            logger.warning("Fixing invalid unit metadata", extra={"original_unit": q.unit, "assigned_unit": req.unit_ids[0]})
            q.unit = req.unit_ids[0]
            
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
    
    return {
        "requested_count": req.count,
        "delivered_count": delivered_count,
        "quiz": quiz_doc
    }

