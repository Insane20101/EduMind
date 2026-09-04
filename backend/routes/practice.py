from fastapi import APIRouter, HTTPException
import os
import glob
from rag.chunker import chunk_markdown

router = APIRouter()

def get_subject_paths(subject_id: str):
    # Search in data/ folder for the subject directory
    base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    search_pattern = os.path.join(base_dir, "**", f"{subject_id} *")
    dirs = glob.glob(search_pattern, recursive=True)
    if not dirs:
        return None, None
    
    subject_dir = dirs[0]
    qb_path = os.path.join(subject_dir, f"{subject_id}_Question_Bank.md")
    
    sol_pattern = os.path.join(subject_dir, f"*Solutions.md")
    sol_files = glob.glob(sol_pattern)
    sol_path = sol_files[0] if sol_files else None
    
    if not os.path.exists(qb_path):
        return None, sol_path
        
    return qb_path, sol_path

@router.get("/api/subjects/{subject_id}/practice")
def get_practice_units(subject_id: str):
    qb_path, _ = get_subject_paths(subject_id)
    if not qb_path:
        return {"available": False}
        
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
    
    return {"available": True, "units": units}

@router.get("/api/subjects/{subject_id}/practice/{unit_id}")
def get_practice_questions(subject_id: str, unit_id: str):
    qb_path, _ = get_subject_paths(subject_id)
    if not qb_path:
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
            
    questions.sort(key=lambda x: int(x["question_id"]))
            
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
            
    raise HTTPException(status_code=404, detail=f"No solution found for unit {unit_id} question {question_id}")
