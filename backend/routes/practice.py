from fastapi import APIRouter, HTTPException
import os
import glob
from rag.chunker import chunk_markdown

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
def get_practice_questions(subject_id: str, unit_id: str):
    qb_path, _ = get_subject_paths(subject_id)
    if not qb_path or not os.path.exists(qb_path):
        raise HTTPException(status_code=404, detail="Question bank not found")
        
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
            
    return {"questions": questions}

@router.get("/api/subjects/{subject_id}/practice/{unit_id}/{question_id}/solution")
def get_practice_solution(subject_id: str, unit_id: str, question_id: str):
    _, sol_path = get_subject_paths(subject_id)
    if not sol_path or not os.path.exists(sol_path):
        raise HTTPException(status_code=404, detail="Solutions not available for this subject")
        
    with open(sol_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    chunks = chunk_markdown(text, os.path.basename(sol_path), subject_id, "unknown", "solutions")
    
    for c in chunks:
        # Check matching unit and question_id
        if c["metadata"].get("unit") == unit_id and str(c["metadata"].get("question_id")) == str(question_id):
            return {"question_id": question_id, "solution_text": c["text"]}
            
    # Sub-fallback if question_id is numeric match
    for c in chunks:
        if str(c["metadata"].get("question_id")) == str(question_id):
            return {"question_id": question_id, "solution_text": c["text"]}

    raise HTTPException(status_code=404, detail=f"No solution found for unit {unit_id} question {question_id}")

