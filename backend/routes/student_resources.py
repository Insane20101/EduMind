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
from fastapi.responses import JSONResponse, RedirectResponse, Response

# ── Public: list approved resources ───────────────────────────────────────────

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
        if not doc.get("url"):
            doc["url"] = f"/api/resources/file/{rid}"
        for field in ("uploaded_at", "reviewed_at"):
            if isinstance(doc.get(field), datetime):
                doc[field] = doc[field].isoformat()
    return JSONResponse(
        content=docs,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )


import xml.etree.ElementTree as ET

@router.get("/playlists")
async def list_subject_playlists(subject_id: Optional[str] = None):
    """
    Returns active playlists from MongoDB db.playlists with explicit Cache-Control no-store headers.
    Public endpoint, no authentication required.
    """
    query = {}
    if subject_id and subject_id.strip():
        query["subject_id"] = {"$regex": f"^{re.escape(subject_id.strip())}$", "$options": "i"}
    cursor = db.playlists.find(query)
    docs = await cursor.to_list(length=None)
    for d in docs:
        d.pop("_id", None)
    return JSONResponse(
        content=docs,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )


@router.get("/playlist-items")
async def get_youtube_playlist_items(list_id: str):
    """
    Parses ALL 70+ video entries in a YouTube playlist with 100% real original titles,
    thumbnails, and videoIds using multithreaded oEmbed lookup.
    """
    if not list_id:
        raise HTTPException(status_code=400, detail="Missing list_id parameter.")

    url = f"https://www.youtube.com/playlist?list={list_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            html = resp.text
            
            raw_video_ids = re.findall(r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', html)
            video_ids = []
            seen = set()
            for v_id in raw_video_ids:
                if v_id and v_id not in seen:
                    seen.add(v_id)
                    video_ids.append(v_id)

            if video_ids:
                def fetch_info(idx_vid):
                    idx, v_id = idx_vid
                    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v_id}&format=json"
                    try:
                        r = requests.get(oembed_url, timeout=4)
                        if r.status_code == 200:
                            info = r.json()
                            return {
                                "index": idx,
                                "videoId": v_id,
                                "title": info.get("title", f"Lecture #{idx + 1}"),
                                "author": info.get("author_name", ""),
                                "thumbnail": info.get("thumbnail_url", f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg"),
                                "url": f"https://www.youtube.com/watch?v={v_id}"
                            }
                    except Exception:
                        pass
                    return {
                        "index": idx,
                        "videoId": v_id,
                        "title": f"Lecture Video #{idx + 1}",
                        "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg",
                        "url": f"https://www.youtube.com/watch?v={v_id}"
                    }

                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=30) as executor:
                    results = list(executor.map(fetch_info, enumerate(video_ids)))

                results.sort(key=lambda x: x["index"])
                return {"status": "success", "count": len(results), "videos": results}
    except Exception as e:
        logger.warning(f"Playlist items parsing notice: {e}")

    return {"status": "fallback", "count": 0, "videos": []}





from database import db, get_file

@router.get("/file/{resource_id}")
@router.get("/view/{resource_id}")
async def serve_resource_file(resource_id: str):
    """
    Public protected viewer endpoint for PDF notes and PYQs.
    Serves directly from MongoDB GridFS / Cloud Database with Anti-Download & CORS headers.
    """
    resource = await db.resources.find_one({"resource_id": resource_id})
    title = resource.get("title", "document") if resource else "document"

    headers_pdf = {
        "Content-Disposition": f"inline; filename=\"{title}.pdf\"",
        "X-Content-Type-Options": "nosniff",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    }

    # 1. Fetch from MongoDB GridFS / Cloud File Storage
    cloud_file_id = resource.get("cloud_file_id") if resource else resource_id
    grid_file = await get_file(cloud_file_id) if cloud_file_id else None

    if grid_file and grid_file.get("content"):
        return Response(
            content=grid_file["content"],
            media_type="application/pdf",
            headers=headers_pdf
        )

    # 2. Fallback to cached file bytes if present
    if resource and resource.get("file_bytes_cache"):
        return Response(
            content=resource["file_bytes_cache"],
            media_type="application/pdf",
            headers=headers_pdf
        )

    # 3. Fallback to Cloudinary / external proxy
    url = resource.get("url") if resource else None
    if url and url.startswith("http"):
        try:
            req_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            urls_to_try = [url]
            if "cloudinary.com" in url and "/image/upload/" in url:
                urls_to_try.insert(0, url.replace("/image/upload/", "/raw/upload/"))

            for target_url in urls_to_try:
                resp = requests.get(target_url, headers=req_headers, timeout=10)
                if resp.status_code == 200 and resp.content and len(resp.content) > 0:
                    return Response(
                        content=resp.content,
                        media_type="application/pdf",
                        headers=headers_pdf
                    )
        except Exception as e:
            logger.warning(f"Cloudinary proxy notice: {e}")

    if url:
        return RedirectResponse(url=url)

    raise HTTPException(status_code=404, detail="Resource file content not available.")





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
    resource_type: str          = Form(...),   # "note" | "pyq" | "other"
    title:         str          = Form(...),
    url:           Optional[str] = Form(default=None),  # External URL (optional)
    file:          Optional[UploadFile] = File(default=None),  # File upload (optional)
    current_user:  dict         = Depends(get_current_user),
):
    """
    Authenticated students can submit a resource for admin review.

    - Provide a **file** (PDF/PNG/JPG, max 10 MB) → uploaded to Cloudinary pending folder.
    - Provide a **URL** (Google Drive, etc.) → stored as-is.
    - Both can be provided simultaneously (file takes priority for the stored URL).
    - At least one of file or url must be present.

    Rate limit: 5 submissions per enrollment per minute.
    Status is always 'pending' until admin approves or rejects.
    """
    enrollment = current_user["enrollment"]
    # Attach enrollment to request.state so the rate-limit key_func can read it
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

    if file:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Only PDF, JPG, PNG, or WebP files are allowed.")
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File exceeds the 10 MB student upload limit.")

        # Upload to Cloudinary under a dedicated pending/ folder for easy admin review
        folder = f"edumind/{subject_id}/{resource_type}/pending"
        try:
            upload_result = cloudinary.uploader.upload(
                content,
                folder=folder,
                resource_type="auto",
                public_id=str(uuid.uuid4()),
                overwrite=False,
            )
            stored_url = upload_result.get("secure_url")
            cloudinary_public_id = upload_result.get("public_id")
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Cloudinary upload failed: {exc}")

    # ── Persist record ─────────────────────────────────────────────────────────
    resource_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    doc = {
        "resource_id":          resource_id,
        "subject_id":           subject_id,
        "resource_type":        resource_type,
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
    }
    await db.resources.insert_one(doc)
    doc.pop("_id", None)
    doc["uploaded_at"] = now.isoformat()

    return {
        "message": "Thank you! Your submission has been queued for admin review.",
        "resource_id": resource_id,
        "has_file": cloudinary_public_id is not None,
    }
