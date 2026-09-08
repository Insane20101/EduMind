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

from database import upload_file, get_file


@router.get("/playlists")
async def get_playlists_for_students(subject_id: Optional[str] = None):
    """
    Returns video course playlists for a subject (public student endpoint).
    Falls back to embedded playlists in db.subjects if db.playlists collection is empty.
    """
    if not subject_id or not subject_id.strip():
        cursor = db.playlists.find({})
        docs = await cursor.to_list(length=None)
        for d in docs:
            d.pop("_id", None)
        return JSONResponse(
            content=docs,
            headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
        )

    clean_sub_id = subject_id.strip().upper()
    query = {"subject_id": {"$regex": f"^{re.escape(clean_sub_id)}$", "$options": "i"}}
    cursor = db.playlists.find(query)
    docs = await cursor.to_list(length=None)
    for d in docs:
        d.pop("_id", None)

    if docs:
        return JSONResponse(
            content=docs,
            headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
        )

    # Fallback to embedded playlists in db.subjects document
    subj = await db.subjects.find_one({"code": {"$regex": f"^{re.escape(clean_sub_id)}$", "$options": "i"}})
    fallback_playlists = []
    if subj and subj.get("playlists"):
        for index, item in enumerate(subj["playlists"]):
            if isinstance(item, dict):
                fallback_playlists.append({
                    "playlist_id": f"seed-{clean_sub_id}-{index}",
                    "subject_id": clean_sub_id,
                    "title": item.get("title") or f"{subj.get('name', 'Course')} - {item.get('channel', 'Lectures')}",
                    "url": item.get("url"),
                    "unit": item.get("channel") or "Full Course",
                })
            elif isinstance(item, str):
                fallback_playlists.append({
                    "playlist_id": f"seed-{clean_sub_id}-{index}",
                    "subject_id": clean_sub_id,
                    "title": f"{subj.get('name', 'Course')} Lectures",
                    "url": item,
                    "unit": "Full Course",
                })

import requests
import xml.etree.ElementTree as ET


PUBLIC_INNERTUBE_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"


def fetch_youtube_playlist_videos(list_id: str):
    """
    Fetches all real YouTube video metadata (videoId, exact title, index, thumbnail) for a playlist ID.
    Supports:
      0. Official YouTube Data API v3 (if YOUTUBE_DATA_API_KEY / YOUTUBE_API_KEY is configured in env).
      1. yt-dlp Flat Playlist Extractor (No API key required, supports full 70+ videos on cloud servers).
      2. Direct Innertube API (Datacenter-proof POST API using public key & continuation tokens).
      3. Atom XML RSS Feed fallback as last resort.
    """
    if "list=" in list_id:
        match = re.search(r'[?&]list=([^&]+)', list_id)
        if match:
            list_id = match.group(1)
            
    list_id = list_id.strip()
    videos = []
    seen_ids = set()
    continuations = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.youtube.com",
        "Referer": f"https://www.youtube.com/playlist?list={list_id}"
    }

    # ── Option 0: Official YouTube Data API v3 (if configured) ─────────────
    yt_official_key = os.getenv("YOUTUBE_DATA_API_KEY") or os.getenv("YOUTUBE_API_KEY")
    if yt_official_key:
        try:
            page_token = None
            while True:
                params = {
                    "part": "snippet",
                    "playlistId": list_id,
                    "maxResults": 50,
                    "key": yt_official_key
                }
                if page_token:
                    params["pageToken"] = page_token
                res = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params=params, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    for item in data.get("items", []):
                        snippet = item.get("snippet", {})
                        v_id = snippet.get("resourceId", {}).get("videoId")
                        title = snippet.get("title", "Lecture Video")
                        if v_id and v_id not in seen_ids:
                            seen_ids.add(v_id)
                            videos.append({
                                "videoId": v_id,
                                "title": title,
                                "index": len(videos) + 1,
                                "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg"
                            })
                    page_token = data.get("nextPageToken")
                    if not page_token or len(videos) >= 500:
                        break
                else:
                    break
            if len(videos) > 0:
                return videos
        except Exception as exc_api:
            logger.warning(f"YouTube Data API v3 fetch note for {list_id}: {exc_api}")

    # ── Option 1: yt-dlp Flat Playlist Extractor (No API Key Needed!) ──────
    try:
        import yt_dlp
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'skip_download': True,
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 10,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'mweb', 'web']
                }
            }
        }
        playlist_url = f"https://www.youtube.com/playlist?list={list_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if info and 'entries' in info:
                for entry in info['entries']:
                    v_id = entry.get('id')
                    title = entry.get('title')
                    if v_id and title and v_id not in seen_ids:
                        seen_ids.add(v_id)
                        videos.append({
                            "videoId": v_id,
                            "title": title,
                            "index": len(videos) + 1,
                            "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg"
                        })
        if len(videos) > 0:
            return videos
    except Exception as exc_ytdlp:
        logger.warning(f"yt-dlp extraction note for {list_id}: {exc_ytdlp}")

    # ── Option 1: Direct Innertube API & Recursive Extraction ──────────────
    def extract_from_json(obj):
        if isinstance(obj, dict):
            # Format A: playlistVideoRenderer
            if "playlistVideoRenderer" in obj:
                pvr = obj["playlistVideoRenderer"]
                v_id = pvr.get("videoId")
                runs = pvr.get("title", {}).get("runs", [])
                t_text = runs[0].get("text") if runs else pvr.get("title", {}).get("simpleText")
                if v_id and v_id not in seen_ids:
                    seen_ids.add(v_id)
                    videos.append({
                        "videoId": v_id,
                        "title": t_text or f"Lecture Video #{len(videos)+1}",
                        "index": len(videos) + 1,
                        "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg"
                    })

            # Format B: lockupViewModel (New YouTube Innertube layout)
            elif "lockupViewModel" in obj:
                lvm = obj["lockupViewModel"]
                v_id = lvm.get("contentId")
                t_text = None
                meta = lvm.get("metadata", {}).get("lockupMetadataViewModel", {})
                t_obj = meta.get("title", {})
                if isinstance(t_obj, dict):
                    t_text = t_obj.get("content")
                
                if not v_id:
                    w_ep = lvm.get("rendererContext", {}).get("commandContext", {}).get("onTap", {}).get("innertubeCommand", {}).get("watchEndpoint", {})
                    v_id = w_ep.get("videoId")

                if v_id and v_id not in seen_ids:
                    seen_ids.add(v_id)
                    videos.append({
                        "videoId": v_id,
                        "title": t_text or f"Lecture Video #{len(videos)+1}",
                        "index": len(videos) + 1,
                        "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg"
                    })

            # Format C: gridVideoRenderer
            elif "gridVideoRenderer" in obj:
                gvr = obj["gridVideoRenderer"]
                v_id = gvr.get("videoId")
                runs = gvr.get("title", {}).get("runs", [])
                t_text = runs[0].get("text") if runs else gvr.get("title", {}).get("simpleText")
                if v_id and v_id not in seen_ids:
                    seen_ids.add(v_id)
                    videos.append({
                        "videoId": v_id,
                        "title": t_text or f"Lecture Video #{len(videos)+1}",
                        "index": len(videos) + 1,
                        "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg"
                    })

            # Continuation Token extraction
            if "continuationCommand" in obj:
                token = obj["continuationCommand"].get("token")
                if token and token not in continuations:
                    continuations.append(token)
            elif "continuationItemRenderer" in obj:
                cir = obj["continuationItemRenderer"]
                c_cmd = cir.get("continuationEndpoint", {}).get("continuationCommand", {})
                token = c_cmd.get("token")
                if token and token not in continuations:
                    continuations.append(token)

            for v in obj.values():
                extract_from_json(v)

        elif isinstance(obj, list):
            for item in obj:
                extract_from_json(item)

    # Call Innertube API directly via POST (bypasses HTML consent redirects on Cloud Datacenters)
    browse_url = f"https://www.youtube.com/youtubei/v1/browse?key={PUBLIC_INNERTUBE_KEY}"
    browse_id = f"VL{list_id}" if not list_id.startswith("VL") else list_id
    payload = {
        "context": {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20260907.06.00",
                "hl": "en",
                "gl": "US"
            }
        },
        "browseId": browse_id
    }

    try:
        r_api = requests.post(browse_url, json=payload, headers=headers, timeout=10)
        if r_api.status_code == 200:
            extract_from_json(r_api.json())
    except Exception as e:
        logger.warning(f"Direct Innertube browse API fetch error: {e}")

    # Fetch continuations if available
    curr_tokens = list(continuations)
    page = 0
    while curr_tokens and page < 15: # safety limit up to ~1500 videos
        page += 1
        token = curr_tokens.pop(0)
        cont_payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20260907.06.00",
                    "hl": "en",
                    "gl": "US"
                }
            },
            "continuation": token
        }
        try:
            r_cont = requests.post(browse_url, json=cont_payload, headers=headers, timeout=10)
            if r_cont.status_code == 200:
                c_data = r_cont.json()
                prev_cont_len = len(continuations)
                extract_from_json(c_data)
                for t in continuations[prev_cont_len:]:
                    if t not in curr_tokens:
                        curr_tokens.append(t)
        except Exception as e:
            logger.warning(f"Innertube continuation error: {e}")

    # ── Option 2: Atom XML RSS Feed Fallback (Last resort) ─────────────────
    if len(videos) == 0:
        rss_url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={list_id}"
        try:
            res_rss = requests.get(rss_url, headers=headers, timeout=10)
            if res_rss.status_code == 200:
                root = ET.fromstring(res_rss.text)
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    vid_id_el = entry.find('{http://www.youtube.com/xml/schemas/2015}videoId')
                    title_el = entry.find('{http://www.youtube.com/xml/schemas/2015}title') or entry.find('{http://www.w3.org/2005/Atom}title')
                    if vid_id_el is not None and vid_id_el.text:
                        vid_id = vid_id_el.text
                        if vid_id not in seen_ids:
                            seen_ids.add(vid_id)
                            title = title_el.text if title_el is not None else f"Lecture Video #{len(videos)+1}"
                            videos.append({
                                "videoId": vid_id,
                                "title": title,
                                "index": len(videos) + 1,
                                "thumbnail": f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg"
                            })
        except Exception as exc_rss:
            logger.warning(f"YouTube RSS feed fallback note for {list_id}: {exc_rss}")

    return videos


@router.get("/playlist-items")
async def get_playlist_items(list_id: str):
    """
    Fetches real YouTube video items (title, videoId, index, thumbnail) for a playlist ID in real-time.
    Supports 60+ videos using multi-stage Innertube API scraping and continuation token pagination.
    """
    if not list_id or not list_id.strip():
        raise HTTPException(status_code=400, detail="list_id is required.")

    videos = fetch_youtube_playlist_videos(list_id)

    return {
        "list_id": list_id,
        "total_videos": len(videos),
        "videos": videos
    }


@router.get("/file/{resource_id}")
async def stream_resource_file(resource_id: str):
    """
    Streams PDF file directly from MongoDB GridFS, cached bytes, or Cloudinary proxy with inline headers.
    """
    doc = await db.resources.find_one({
        "$or": [
            {"resource_id": resource_id},
            {"cloud_file_id": resource_id},
            {"cloudinary_public_id": resource_id}
        ]
    })
    
    # 1. GridFS Direct Lookup by file_id if doc not found by resource_id
    if not doc:
        file_obj = await get_file(resource_id)
        if file_obj and file_obj.get("content"):
            return Response(
                content=file_obj["content"],
                media_type="application/pdf",
                headers={
                    "Content-Disposition": "inline; filename=\"document.pdf\"",
                    "Cache-Control": "public, max-age=86400",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        raise HTTPException(status_code=404, detail="Resource document not found.")

    # 2. GridFS storage from document metadata
    cloud_file_id = doc.get("cloud_file_id")
    if cloud_file_id:
        file_obj = await get_file(cloud_file_id)
        if file_obj and file_obj.get("content"):
            filename = file_obj.get("filename") or doc.get("filename") or doc.get("title", "document") + ".pdf"
            return Response(
                content=file_obj["content"],
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"inline; filename=\"{filename}\"",
                    "Cache-Control": "public, max-age=86400",
                    "Access-Control-Allow-Origin": "*"
                }
            )

    # 3. File bytes cache
    cached_bytes = doc.get("file_bytes_cache")
    if cached_bytes:
        filename = doc.get("filename") or doc.get("title", "document") + ".pdf"
        return Response(
            content=cached_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=\"{filename}\"",
                "Cache-Control": "public, max-age=86400",
                "Access-Control-Allow-Origin": "*"
            }
        )

    # 4. Cloudinary or external URL proxy
    target_url = doc.get("url") or doc.get("cloudinary_url")
    if target_url and target_url.startswith("http"):
        try:
            resp = requests.get(target_url, timeout=15)
            if resp.status_code == 200:
                filename = doc.get("filename") or doc.get("title", "document") + ".pdf"
                return Response(
                    content=resp.content,
                    media_type="application/pdf",
                    headers={
                        "Content-Disposition": f"inline; filename=\"{filename}\"",
                        "Cache-Control": "public, max-age=86400",
                        "Access-Control-Allow-Origin": "*"
                    }
                )
        except Exception as exc:
            logger.warning(f"Cloudinary proxy stream error for resource {resource_id}: {exc}")

    raise HTTPException(status_code=404, detail="File content unavailable.")

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
