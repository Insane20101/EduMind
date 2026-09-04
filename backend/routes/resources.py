"""
Admin and Student resource management routes.
Handles uploads, playlists, student community submissions, vector knowledge base curation, and approvals.
"""

import os
import uuid
import logging
import traceback
from datetime import datetime, timezone
from typing import Optional, List

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile

from database import db, upload_file, delete_file
from qdrant_client.http import models

from jwt_utils import get_current_admin_user
from ingestion_queue import ingestion_queue
from rag.ingester import ingest_document
from rag.vector_store import get_qdrant_client, delete_resource_chunks

logger = logging.getLogger(__name__)
router = APIRouter()

# ── Cloudinary config ──────────────────────────────────────────────────────────
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
    "text/plain",
    "text/markdown",
    "application/octet-stream"
}
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "webp", "md", "txt"}
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB


async def get_resources_for_subject(subject_id: str, resource_type: str) -> list:
    """Return approved resources for a subject, filtered by type."""
    cursor = db.resources.find(
        {"subject_id": subject_id, "resource_type": resource_type, "status": "approved"}
    )
    docs = await cursor.to_list(length=None)
    for doc in docs:
        doc.pop("_id", None)
        for field in ("uploaded_at", "reviewed_at"):
            if isinstance(doc.get(field), datetime):
                doc[field] = doc[field].isoformat()
    return docs


# ── Student Community Submission Endpoint ──────────────────────────────────────

@router.post("/community-upload")
@router.post("/suggest")
async def student_community_upload(

    subject_id: str = Form(...),
    title: str = Form(...),
    resource_type: str = Form("note"),
    submitter_enrollment: str = Form("Anonymous Student"),
    file: UploadFile = File(...)
):
    """Students/Users submit notes or resources — enters pending approval queue."""
    filename = file.filename or "student_submission"
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file format '.{ext}'. Supported formats: PDF, MD, TXT, JPG, PNG.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds 15 MB limit.")

    # Upload to Cloudinary (or local storage fallback)
    url = ""
    public_id = None
    try:
        if os.getenv("CLOUDINARY_CLOUD_NAME"):
            folder = f"edumind/community/{subject_id}"
            res_type = "raw" if ext == "pdf" else "auto"
            upload_result = cloudinary.uploader.upload(
                content,
                folder=folder,
                resource_type=res_type,
                public_id=str(uuid.uuid4()),
                overwrite=False
            )
            url = upload_result.get("secure_url", "")
            public_id = upload_result.get("public_id")
    except Exception as e:
        logger.warning(f"Cloudinary upload fallback: {e}")

    cloud_file_id = None
    try:
        cloud_file_id = await upload_file(filename, content, "application/pdf")
    except Exception as e:
        logger.warning(f"GridFS upload note: {e}")

    resource_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    doc = {
        "resource_id": resource_id,
        "cloud_file_id": cloud_file_id,
        "subject_id": subject_id.upper(),
        "resource_type": resource_type,
        "title": title,
        "filename": filename,
        "url": url,
        "cloudinary_public_id": public_id,
        "status": "pending",
        "uploaded_by": submitter_enrollment,
        "uploaded_at": now,
        "reviewed_by": None,
        "reviewed_at": None,
        "reject_reason": None,
        "source": "student",
        "submitter_enrollment": submitter_enrollment,
        "file_bytes_cache": content  # Cached for ingestion on admin approval
    }

    await db.resources.insert_one(doc)
    doc.pop("_id", None)
    doc.pop("file_bytes_cache", None)
    return doc


# ── Admin Resource Endpoints ───────────────────────────────────────────────────

@router.post("/upload")
async def admin_upload_resource(
    subject_id: str = Form(...),
    resource_type: str = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    current_admin: dict = Depends(get_current_admin_user)
):
    """Admin uploads resource — automatically acquires single-task lock and ingests to ChromaDB."""
    filename = file.filename or "admin_resource"
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file format.")

    if not ingestion_queue.acquire_lock(filename):
        raise HTTPException(status_code=429, detail="An ingestion task is currently in progress! Please wait until it completes.")

    try:
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File exceeds 15 MB limit.")

        ingestion_queue.update_progress(30, f"Running unified ingestion for '{filename}'...")

        # Ingest to ChromaDB via unified single ingestion pipeline
        ingest_summary = ingest_document(
            content_bytes=content,
            filename=filename,
            subject_id=subject_id,
            unit_id=None,
            resource_type=resource_type
        )

        ingestion_queue.update_progress(70, "Uploading resource to Cloudinary CDN...")

        url = ""
        public_id = None
        try:
            if os.getenv("CLOUDINARY_CLOUD_NAME"):
                folder = f"edumind/{subject_id}/{resource_type}"
                res_type = "raw" if ext == "pdf" else "auto"
                upload_result = cloudinary.uploader.upload(
                    content,
                    folder=folder,
                    resource_type=res_type,
                    public_id=str(uuid.uuid4()),
                    overwrite=False
                )
                url = upload_result.get("secure_url", "")
                public_id = upload_result.get("public_id")
        except Exception as e:
            logger.warning(f"Cloudinary upload note: {e}")

        resource_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        # Store file in MongoDB GridFS / Cloud DB (No local disk storage)
        cloud_file_id = await upload_file(filename, content, "application/pdf")

        doc = {
            "resource_id": resource_id,
            "cloud_file_id": cloud_file_id,
            "subject_id": subject_id.upper(),
            "resource_type": resource_type,
            "title": title,
            "filename": filename,
            "url": url,
            "cloudinary_public_id": public_id,
            "status": "approved",
            "uploaded_by": current_admin["admin_id"],
            "uploaded_at": now,
            "reviewed_by": current_admin["admin_id"],
            "reviewed_at": now,
            "reject_reason": None,
            "source": "admin",
            "submitter_enrollment": None,
            "ingest_summary": ingest_summary
        }
        await db.resources.insert_one(doc)
        doc.pop("_id", None)

        ingestion_queue.release_lock(success=True, final_message=f"Successfully ingested '{filename}' ({ingest_summary['chunk_count']} chunks).")
        return doc
    except Exception as e:
        tb_str = traceback.format_exc()
        logger.error(f"ADMIN UPLOAD EXCEPTION: [{type(e).__name__}] {str(e)}\n{tb_str}")
        ingestion_queue.release_lock(success=False, final_message=f"Ingestion error: [{type(e).__name__}] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: [{type(e).__name__}] {str(e)}")


@router.get("/")
async def admin_list_resources(
    status: Optional[str] = None,
    subject_id: Optional[str] = None,
    current_admin: dict = Depends(get_current_admin_user)
):
    """List resources filtered by status and/or subject."""
    query = {}
    if status:
        query["status"] = status
    if subject_id:
        query["subject_id"] = subject_id.upper()

    cursor = db.resources.find(query)
    docs = await cursor.to_list(length=None)
    for doc in docs:
        doc.pop("_id", None)
        doc.pop("file_bytes_cache", None)
        rid = doc.get("resource_id")
        doc["file_url"] = f"/api/resources/file/{rid}"
        if not doc.get("url"):
            doc["url"] = f"/api/resources/file/{rid}"
        for field in ("uploaded_at", "reviewed_at"):

            if isinstance(doc.get(field), datetime):
                doc[field] = doc[field].isoformat()
    return docs


@router.get("/ingestion-status")
async def get_ingestion_lock_status():
    """Public status endpoint for single-task processing lock banner."""
    return ingestion_queue.get_status()


@router.post("/{resource_id}/approve")
async def approve_resource(
    resource_id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Approve pending student resource and run single-task vector ingestion."""
    doc = await db.resources.find_one({"resource_id": resource_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Resource not found.")
    if doc["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Resource is already '{doc['status']}'.")

    filename = doc.get("filename") or (doc.get("title", "student_resource") + ".pdf")
    if not ingestion_queue.acquire_lock(filename):
        raise HTTPException(status_code=429, detail="An ingestion task is currently running! Please wait before approving.")

    try:
        content_bytes = doc.get("file_bytes_cache")
        if not content_bytes:
            content_bytes = f"# {doc.get('title')}\n\nSubmitted by student {doc.get('submitter_enrollment')}".encode("utf-8")

        ingest_summary = ingest_document(
            content_bytes=content_bytes,
            filename=filename,
            subject_id=doc["subject_id"],
            unit_id=None,
            resource_type=doc.get("resource_type", "note")
        )

        cloud_file_id = doc.get("cloud_file_id")
        if not cloud_file_id and content_bytes:
            try:
                cloud_file_id = await upload_file(filename, content_bytes, "application/pdf")
            except Exception as e:
                logger.warning(f"GridFS approval upload: {e}")

        now = datetime.now(timezone.utc)
        update_set = {
            "status": "approved",
            "reviewed_by": current_admin["admin_id"],
            "reviewed_at": now,
            "reject_reason": None,
            "ingest_summary": ingest_summary
        }
        if cloud_file_id:
            update_set["cloud_file_id"] = cloud_file_id

        await db.resources.update_one(
            {"resource_id": resource_id},
            {"$set": update_set}
        )

        ingestion_queue.release_lock(success=True, final_message=f"Approved and ingested '{filename}'.")
        return {"message": "Resource approved and ingested into vector database.", "resource_id": resource_id}
    except Exception as e:
        ingestion_queue.release_lock(success=False, final_message=f"Approval ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Approval failed: {str(e)}")


@router.post("/{resource_id}/reject")
async def reject_resource(
    resource_id: str,
    reason: str = Form(default=""),
    current_admin: dict = Depends(get_current_admin_user)
):
    """Reject pending student submission."""
    doc = await db.resources.find_one({"resource_id": resource_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Resource not found.")
    if doc["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Resource is already '{doc['status']}'.")

    now = datetime.now(timezone.utc)
    await db.resources.update_one(
        {"resource_id": resource_id},
        {"$set": {
            "status": "rejected",
            "reviewed_by": current_admin["admin_id"],
            "reviewed_at": now,
            "reject_reason": reason or "No reason provided.",
        }}
    )
    return {"message": "Resource rejected.", "resource_id": resource_id}


@router.delete("/{resource_id}")
async def delete_resource(
    resource_id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Permanently delete a resource, including GridFS storage, Cloudinary mirror, and ChromaDB vector chunks."""
    doc = await db.resources.find_one({"resource_id": resource_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Resource not found.")

    subject_id = doc.get("subject_id")
    filename = doc.get("filename") or doc.get("title")
    purged_chunks = 0

    # 1. Purge matching vector chunks from target subject's Qdrant Cloud collection
    if subject_id:
        try:
            purged_chunks = delete_resource_chunks(subject_id=subject_id, resource_id=resource_id, source_filename=filename)
            logger.info(f"Purged {purged_chunks} vector chunks for '{filename}' (resource_id={resource_id}) from Qdrant Cloud collection '{subject_id}'.")
        except Exception as e:
            logger.warning(f"Qdrant Cloud vector purge note for resource {resource_id}: {e}")

    # 2. Cloudinary mirror cleanup
    public_id = doc.get("cloudinary_public_id")
    if public_id:
        try:
            cloudinary.uploader.destroy(public_id, resource_type="raw")
        except Exception:
            pass

    # 3. GridFS file storage cleanup
    cloud_file_id = doc.get("cloud_file_id")
    if cloud_file_id:
        try:
            await delete_file(cloud_file_id)
        except Exception:
            pass

    # 4. Remove metadata record from MongoDB
    await db.resources.delete_many({"resource_id": resource_id})
    return {
        "message": "Resource and associated vector chunks permanently deleted.",
        "resource_id": resource_id,
        "purged_chunks_count": purged_chunks
    }


# ── Admin Playlist Endpoints (MongoDB db.playlists Migration) ──────────────────

@router.get("/playlists")
async def get_playlists(
    subject_id: Optional[str] = None,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Fetch video course playlists from MongoDB db.playlists."""

    query = {}
    if subject_id:
        query["subject_id"] = subject_id.upper()
    cursor = db.playlists.find(query)
    docs = await cursor.to_list(length=None)
    for d in docs:
        d.pop("_id", None)
    return docs


@router.post("/playlists")
async def update_playlist(
    subject_id: str = Form(...),
    title: str = Form(...),
    playlist_url: str = Form(...),
    unit: str = Form("Unit 1"),
    current_admin: dict = Depends(get_current_admin_user)
):
    """Admin creates/updates a subject playlist entry in db.playlists."""
    playlist_id = str(uuid.uuid4())
    doc = {
        "playlist_id": playlist_id,
        "subject_id": subject_id.upper(),
        "title": title,
        "url": playlist_url,
        "unit": unit,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "updated_by": current_admin["admin_id"]
    }
    await db.playlists.insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.delete("/playlists/{playlist_id}")
async def delete_playlist(
    playlist_id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Admin deletes a playlist entry."""
    res = await db.playlists.delete_many({"playlist_id": playlist_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Playlist entry not found.")
    return {"message": "Playlist deleted.", "playlist_id": playlist_id}


# ── Vector Knowledge Base Curator Endpoints ────────────────────────────────────

@router.get("/vector/chunks")
async def list_vector_chunks(
    subject_id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Inspect ingested Qdrant Cloud vector chunks for a specific subject collection."""
    if not subject_id or not subject_id.strip():
        raise HTTPException(status_code=400, detail="subject_id is required.")

    subject_id = subject_id.strip().upper()
    client = get_qdrant_client()

    if not client.collection_exists(subject_id):
        return {
            "subject_id": subject_id,
            "collection_name": subject_id,
            "total_chunks": 0,
            "chunks": []
        }

    try:
        points, _ = client.scroll(
            collection_name=subject_id,
            limit=100,
            with_payload=True,
            with_vectors=False
        )
    except Exception as e:
        logger.warning(f"Qdrant scroll error for collection {subject_id}: {e}")
        points = []

    chunks = []
    for pt in points:
        payload = pt.payload or {}
        text_snippet = payload.get("text") or payload.get("page_content") or ""
        meta = {k: v for k, v in payload.items() if k not in ("text", "page_content")}
        chunks.append({
            "chunk_id": str(pt.id),
            "metadata": meta,
            "snippet": text_snippet[:200]
        })

    return {
        "subject_id": subject_id,
        "collection_name": subject_id,
        "total_chunks": len(chunks),
        "chunks": chunks
    }


@router.post("/vector/ingest-md")
async def admin_ingest_markdown(
    subject_id: str = Form(...),
    unit: Optional[str] = Form(None),
    title: str = Form(...),
    file: UploadFile = File(...),
    current_admin: dict = Depends(get_current_admin_user)
):
    """Admin uploads custom Markdown/Text file directly into Qdrant Cloud using unified ingester."""
    filename = file.filename or f"{title}.md"
    if not ingestion_queue.acquire_lock(filename):
        raise HTTPException(status_code=429, detail="An ingestion task is currently running! Please wait.")

    try:
        content = await file.read()
        summary = ingest_document(
            content_bytes=content,
            filename=filename,
            subject_id=subject_id,
            unit_id=unit,
            resource_type="admin_curated_note"
        )
        ingestion_queue.release_lock(success=True, final_message=f"Curated document '{filename}' ingested successfully.")
        return summary
    except Exception as e:
        ingestion_queue.release_lock(success=False, final_message=f"Curation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/vector/chunks/{subject_id}/{filename:path}")
async def scoped_delete_vector_chunks(
    subject_id: str,
    filename: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    """Scoped deletion of file chunks from target subject collection ONLY."""
    if not subject_id or not filename:
        raise HTTPException(status_code=400, detail="subject_id and filename are required.")

    subject_id = subject_id.strip().upper()
    deleted_count = delete_resource_chunks(subject_id=subject_id, source_filename=filename)

    if deleted_count > 0:
        return {
            "message": f"Purged {deleted_count} chunks for '{filename}' from subject collection '{subject_id}'.",
            "subject_id": subject_id,
            "filename": filename,
            "deleted_count": deleted_count
        }
    else:
        raise HTTPException(status_code=404, detail=f"No vector chunks found for '{filename}' in subject '{subject_id}'.")
