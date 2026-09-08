"""
Student-facing resource routes.
  GET  /api/resources         — list approved resources (public, no auth required)
  POST /api/resources/suggest — student submits a resource (optional file upload OR URL)
                                 Rate-limited: 5 suggestions per enrollment per minute.
"""

import os
import re
import uuid
import json
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)



import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from database import db
from jwt_utils import get_current_user
from limiter import limiter

router = APIRouter()

# ── Cloudinary config ──────────────────────────────────────────────────────────
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

ALLOWED_MIME_TYPES = {"application/pdf", "image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB cap for student uploads


import requests
from fastapi.responses import Response, StreamingResponse

@router.get("/")
async def list_approved_resources(
    subject_id: Optional[str] = None,
    resource_type: Optional[str] = None,
):
    """
    Returns all approved resources with explicit Cache-Control no-store headers.
    Optionally filtered by subject_id and/or resource_type.
    No authentication required.
    """
    query: dict = {"status": "approved"}
    if subject_id and subject_id.strip():
        query["subject_id"] = {"$regex": f"^{re.escape(subject_id.strip())}$", "$options": "i"}
    if resource_type and resource_type.strip():
        query["resource_type"] = resource_type.strip().lower()

    cursor = db.resources.find(query)
    docs = await cursor.to_list(length=None)
    for doc in docs:
        doc.pop("_id", None)
        rid = doc.get("resource_id")
        doc["file_url"] = f"/api/resources/file/{rid}"
        # For document/file resources, ensure URL routes to protected PDF file endpoint
        raw_url = doc.get("url", "")
        if not raw_url or ("cloudinary.com" in raw_url and raw_url.endswith(".pdf")):
            doc["url"] = f"/api/resources/file/{rid}"
        for field in ("uploaded_at", "reviewed_at"):
            if isinstance(doc.get(field), datetime):
                doc[field] = doc[field].isoformat()
    return JSONResponse(
        content=docs,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )

from database import upload_file

# ── Authenticated: student submits a resource ──────────────────────────────────

def _enrollment_key(request: Request) -> str:
    """Rate-limit key: enrollment number from request state (set after JWT check)."""
    return getattr(request.state, "enrollment", None) or request.client.host


@router.post("/suggest")
@router.post("/community-upload")
@limiter.limit("5/minute", key_func=_enrollment_key)
async def suggest_resource(
    request: Request,
    # Form fields
    subject_id:    str          = Form(...),
    resource_type: str          = Form(...),   # "note" | "pyq" | "playlist" | "other"
    title:         str          = Form(...),
    url:           Optional[str] = Form(default=None),  # External URL (optional)
    file:          Optional[UploadFile] = File(default=None),  # File upload (optional)
    current_user:  dict         = Depends(get_current_user),
):
    """
    Authenticated students can submit a resource or playlist for admin review.
    """
    enrollment = current_user["enrollment"]
    request.state.enrollment = enrollment

    # ── Validation ─────────────────────────────────────────────────────────────
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty.")
    if not file and not (url and url.strip()):
        raise HTTPException(status_code=400, detail="Provide either a file or a URL (or both).")

    # Verify the subject exists
    subject_doc = await db.subjects.find_one({"code": subject_id})
    if not subject_doc:
        raise HTTPException(status_code=404, detail="Subject not found.")

    # ── Handle file upload ─────────────────────────────────────────────────────
    stored_url = url.strip() if url and url.strip() else None
    cloudinary_public_id = None
    cloud_file_id = None
    content_bytes = None

    if file:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Only PDF, JPG, PNG, or WebP files are allowed.")
        content_bytes = await file.read()
        if len(content_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File exceeds the 10 MB student upload limit.")

        filename = file.filename or "student_submission.pdf"
        ext = filename.split(".")[-1].lower() if "." in filename else ""

        # Upload to GridFS for instant guaranteed PDF serving
        try:
            cloud_file_id = await upload_file(filename, content_bytes, "application/pdf")
        except Exception as grid_err:
            logger.warning(f"GridFS upload notice for student submission: {grid_err}")

        # Upload to Cloudinary under dedicated pending folder
        folder = f"edumind/{subject_id}/{resource_type}/pending"
        try:
            res_type = "raw" if ext == "pdf" or file.content_type == "application/pdf" else "auto"
            upload_result = cloudinary.uploader.upload(
                content_bytes,
                folder=folder,
                resource_type=res_type,
                public_id=str(uuid.uuid4()),
                overwrite=False,
            )
            stored_url = upload_result.get("secure_url") or stored_url
            cloudinary_public_id = upload_result.get("public_id")
        except Exception as exc:
            logger.warning(f"Cloudinary upload fallback for student submission: {exc}")

    # ── Persist record ─────────────────────────────────────────────────────────
    resource_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    doc = {
        "resource_id":          resource_id,
        "cloud_file_id":        cloud_file_id,
        "subject_id":           subject_id.upper(),
        "resource_type":        resource_type.strip().lower(),
        "title":                title.strip(),
        "url":                  stored_url,
        "cloudinary_public_id": cloudinary_public_id,
        "status":               "pending",
        "uploaded_by":          enrollment,
        "uploaded_at":          now,
        "reviewed_by":          None,
        "reviewed_at":          None,
        "reject_reason":        None,
        "source":               "student",
        "submitter_enrollment": enrollment,
        "file_bytes_cache":     content_bytes
    }
    await db.resources.insert_one(doc)
    doc.pop("_id", None)
    doc.pop("file_bytes_cache", None)
    doc["uploaded_at"] = now.isoformat()

    return {
        "message": "Thank you! Your submission has been queued for admin review.",
        "resource_id": resource_id,
        "has_file": cloud_file_id is not None or cloudinary_public_id is not None,
    }
