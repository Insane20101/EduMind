from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict
from database import db
from schemas import Subject
from routes.resources import get_resources_for_subject

router = APIRouter()

def normalize_semester(semester: str) -> str:
    """Accepts '1', 'Semester-1', 'Semester 1' -> returns 'Semester-1'."""
    s = semester.strip()
    if s.lower().startswith("semester"):
        s = s.replace("Semester", "").replace("-", " ").strip()
    return f"Semester-{s}"

@router.get("/", response_model=Dict[str, List[Subject]])
async def get_all_subjects():
    cursor = db.subjects.find({})
    docs = await cursor.to_list(length=None)
    grouped: Dict[str, List[dict]] = {}
    for doc in docs:
        doc.pop("_id", None)
        grouped.setdefault(doc["semester"], []).append(doc)
    return grouped

@router.get("/{semester}", response_model=List[Subject])
async def get_subjects_by_semester(semester: str):
    key = normalize_semester(semester)
    cursor = db.subjects.find({"semester": key})
    docs = await cursor.to_list(length=None)
    if not docs:
        raise HTTPException(status_code=404, detail=f"No subjects found for {key}")
    for doc in docs:
        doc.pop("_id", None)
    return docs

@router.get("/{subject_id}/notes")
async def get_subject_notes(subject_id: str):
    """
    DEPRECATED — still functional, but use GET /api/resources?subject_id={id}&resource_type=note.
    Returns data with Deprecation + Warning headers so existing clients don't break.
    """
    resources = await get_resources_for_subject(subject_id, "note")
    return JSONResponse(
        content={"available": len(resources) > 0, "resources": resources},
        headers={
            "Deprecation": "true",
            "Link": f'</api/resources?subject_id={subject_id}&resource_type=note>; rel="successor-version"',
            "Warning": '299 - "This endpoint is deprecated. Use GET /api/resources?subject_id=<id>&resource_type=note"',
        },
    )

@router.get("/{subject_id}/pyqs")
async def get_subject_pyqs(subject_id: str):
    """
    DEPRECATED — still functional, but use GET /api/resources?subject_id={id}&resource_type=pyq.
    Returns data with Deprecation + Warning headers so existing clients don't break.
    """
    resources = await get_resources_for_subject(subject_id, "pyq")
    return JSONResponse(
        content={"available": len(resources) > 0, "resources": resources},
        headers={
            "Deprecation": "true",
            "Link": f'</api/resources?subject_id={subject_id}&resource_type=pyq>; rel="successor-version"',
            "Warning": '299 - "This endpoint is deprecated. Use GET /api/resources?subject_id=<id>&resource_type=pyq"',
        },
    )

