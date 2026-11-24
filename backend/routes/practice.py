from fastapi import APIRouter, HTTPException
import os
import glob
import json
import time
import uuid
from rag.chunker import chunk_markdown
from database import db
from rag.retriever import retrieve
from rag.generator import generate_with_retry
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

STANDARD_UNITS = ["Unit I", "Unit II", "Unit III", "Unit IV"]

def get_subject_paths(subject_id: str):
    if not subject_id:
        return None, None
        
    subject_id_clean = subject_id.strip().upper()
    subj_no_hyphen = subject_id_clean.replace("-", "")
    
    # Base data directory search — robust resolution for local and Render production
    candidate_dirs = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")),
        os.path.abspath(os.path.join(os.getcwd(), "data")),
        os.path.abspath(os.path.join(os.getcwd(), "..", "data")),
        os.path.abspath("data")
    ]
    
    base_dir = None
    for d in candidate_dirs:
        if os.path.exists(d) and os.path.isdir(d):
            base_dir = d
            break
            
    if not base_dir:
        return None, None
        
    matching_dir = None
    for root, dirs, files in os.walk(base_dir):
        dirname = os.path.basename(root).upper()
        dir_clean = dirname.replace("-", "")
        if subject_id_clean in dirname or subj_no_hyphen in dir_clean:
            matching_dir = root
            break
            
    if not matching_dir:
        return None, None
        
    qb_path = None
    sol_path = None
    
    for f in os.listdir(matching_dir):
        f_lower = f.lower()
        full_p = os.path.join(matching_dir, f)
        if not f_lower.endswith(".md"):
            continue
        if "syllabus" in f_lower:
            continue
        if "solution" in f_lower or "sol" in f_lower:
            sol_path = full_p
        elif "question" in f_lower or "qbank" in f_lower or "qb" in f_lower or "practice" in f_lower:
            qb_path = full_p
            
    if not qb_path and sol_path:
        qb_path = sol_path
    if not sol_path and qb_path:
        sol_path = qb_path
        
    return qb_path, sol_path

@router.get("/api/subjects/{subject_id}/practice")
def get_practice_units(subject_id: str):
    qb_path, _ = get_subject_paths(subject_id)
    
    if not qb_path or not os.path.exists(qb_path):
        # Fallback to standard units so quiz generator and practice unit scope are always available
        units = [{"unit_id": u, "count": 5} for u in STANDARD_UNITS]
        return {"available": True, "has_qbank": False, "units": units}
        
    with open(qb_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    chunks = chunk_markdown(text, os.path.basename(qb_path), subject_id, "unknown", "question_bank")
    
    unit_counts = {}
    for c in chunks:
        unit = c["metadata"].get("unit", "unassigned")
        if unit == "unassigned" or "question_id" not in c["metadata"]:
            continue
        unit_counts[unit] = unit_counts.get(unit, 0) + 1
        
    units = [{"unit_id": u, "count": c} for u, c in unit_counts.items()]
    units.sort(key=lambda x: x["unit_id"])
    
    if not units:
        units = [{"unit_id": u, "count": 5} for u in STANDARD_UNITS]
        
    return {"available": True, "has_qbank": True, "units": units}

@router.get("/api/subjects/{subject_id}/practice/{unit_id}")
async def get_practice_questions(subject_id: str, unit_id: str):
    qb_path, _ = get_subject_paths(subject_id)
    if qb_path and os.path.exists(qb_path):
        with open(qb_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        chunks = chunk_markdown(text, os.path.basename(qb_path), subject_id, "unknown", "question_bank")
        questions = []
        for c in chunks:
            if c["metadata"].get("unit") == unit_id and "question_id" in c["metadata"]:
                questions.append({
                    "question_id": c["metadata"]["question_id"],
                    "metadata": c["metadata"],
                    "question_text": c["text"]
                })
                
        questions.sort(key=lambda x: int(x["question_id"]) if str(x["question_id"]).isdigit() else 0)
        if questions:
            return {"questions": questions}

    # Fallback to MongoDB or dynamic AI generation
    subject_clean = subject_id.strip().upper()
    quizzes = await db.quizzes.find({"subject_id": subject_clean}).to_list(length=30)
    db_questions = []
    for q_doc in quizzes:
        for q_item in q_doc.get("questions", []):
            q_unit = str(q_item.get("unit") or "")
            if unit_id.lower() in q_unit.lower() or unit_id.replace(" ", "").lower() in q_unit.replace(" ", "").lower():
                db_questions.append({
                    "question_id": q_item.get("question_id") or str(len(db_questions) + 1),
                    "metadata": {"unit": unit_id, "difficulty": q_item.get("difficulty", "Medium")},
                    "question_text": q_item.get("question_text") or q_item.get("question")
                })
    if db_questions:
        return {"questions": db_questions[:10]}

    # Dynamic AI synthesis
    all_chunks = retrieve(subject_id=subject_clean, unit_id=unit_id, query=f"{unit_id} university practice questions and derivations", top_k=3)
    ctx = "\n".join([c["text"][:300] for c in all_chunks])
    prompt = f"""You are a university professor for course '{subject_clean}'.
Generate 5 high-quality standard academic practice questions for '{unit_id}'.
Context:
{ctx if ctx else f"Syllabus concepts for {subject_clean} {unit_id}"}

Return strictly a JSON array of objects:
[
  {{
    "question_id": "1",
    "question_text": "...",
    "solution_text": "Detailed step-by-step solution..."
  }}
]"""
    ai_qs = []
    try:
        raw = generate_with_retry(prompt, is_json=True)
        if raw:
            clean = raw.strip()
            if clean.startswith("```json"): clean = clean[7:]
            if clean.startswith("```"): clean = clean[3:]
            if clean.endswith("```"): clean = clean[:-3]
            parsed = json.loads(clean.strip())
            for idx, item in enumerate(parsed):
                if item.get("question_text"):
                    ai_qs.append({
                        "question_id": str(idx + 1),
                        "metadata": {"unit": unit_id, "difficulty": "Medium"},
                        "question_text": item["question_text"],
                        "solution_text": item.get("solution_text")
                    })
    except Exception as e:
        logger.warning(f"Dynamic practice question gen notice: {e}")

    if not ai_qs:
        ai_qs = [
            {
                "question_id": "1",
                "metadata": {"unit": unit_id, "difficulty": "Medium"},
                "question_text": f"Define the core theoretical principles and boundary conditions governing {unit_id} in {subject_clean}.",
                "solution_text": f"Step 1: Identify governing laws in {unit_id}.\nStep 2: Formulate boundary assumptions.\nStep 3: State final mathematical relationships."
            },
            {
                "question_id": "2",
                "metadata": {"unit": unit_id, "difficulty": "Medium"},
                "question_text": f"Derive the standard governing formula and analyze its parameter sensitivity in {unit_id}.",
                "solution_text": f"Step 1: State the primary formulation.\nStep 2: Differentiate with respect to parameters.\nStep 3: Analyze stability criteria."
            }
        ]

    try:
        await db.quizzes.insert_one({
            "subject_id": subject_clean,
            "title": f"{subject_clean} {unit_id} Standard Practice",
            "questions": [{
                "question_id": q["question_id"],
                "unit": unit_id,
                "question_text": q["question_text"],
                "solution": q.get("solution_text")
            } for q in ai_qs],
            "created_at": time.time()
        })
    except Exception:
        pass

    return {"questions": ai_qs}

@router.get("/api/subjects/{subject_id}/practice/{unit_id}/{question_id}/solution")
async def get_practice_solution(subject_id: str, unit_id: str, question_id: str):
    _, sol_path = get_subject_paths(subject_id)
    if sol_path and os.path.exists(sol_path):
        with open(sol_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        chunks = chunk_markdown(text, os.path.basename(sol_path), subject_id, "unknown", "solutions")
        for c in chunks:
            if c["metadata"].get("unit") == unit_id and str(c["metadata"].get("question_id")) == str(question_id):
                return {"question_id": question_id, "solution_text": c["text"]}
        for c in chunks:
            if str(c["metadata"].get("question_id")) == str(question_id):
                return {"question_id": question_id, "solution_text": c["text"]}

    # Fallback to MongoDB or dynamic generator
    subject_clean = subject_id.strip().upper()
    quizzes = await db.quizzes.find({"subject_id": subject_clean}).to_list(length=30)
    for q_doc in quizzes:
        for q_item in q_doc.get("questions", []):
            if str(q_item.get("question_id")) == str(question_id):
                sol = q_item.get("solution") or q_item.get("solution_text") or q_item.get("explanation")
                if sol:
                    return {"question_id": question_id, "solution_text": sol}

    chunks = retrieve(subject_id=subject_clean, unit_id=unit_id, query=f"solution for question {question_id} {unit_id}", top_k=3)
    ctx = "\n".join([c["text"][:300] for c in chunks])
    prompt = f"""You are a university professor. Provide a detailed, step-by-step academic solution and derivation for Question {question_id} in {subject_clean} {unit_id}.
Course Context:
{ctx}
Provide clear steps (Step 1, Step 2, etc.) and formulas."""
    try:
        sol_text = generate_with_retry(prompt)
        if sol_text:
            return {"question_id": question_id, "solution_text": sol_text}
    except Exception:
        pass

    return {
        "question_id": question_id,
        "solution_text": f"Step 1: Review governing syllabus definitions for {unit_id}.\nStep 2: Apply parameter constraints and boundary conditions.\nStep 3: Conclude final analytical result."
    }

