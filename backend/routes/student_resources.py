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
from typing import Optional, List
import requests
from pydantic import BaseModel

logger = logging.getLogger(__name__)

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, Response
from fastapi.responses import JSONResponse

from database import db, upload_file, get_file
from jwt_utils import get_current_user
from limiter import limiter

from utils.pdf_compressor import compress_pdf_bytes

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

def format_iso(dt):
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            return dt.isoformat() + "Z"
        return dt.isoformat()
    return dt


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
        doc.pop("file_bytes_cache", None)
        rid = doc.get("resource_id")
        doc["file_url"] = f"/api/resources/file/{rid}"
        # For document/file resources, ensure URL routes to protected PDF file endpoint
        raw_url = doc.get("url", "")
        if not raw_url or ("cloudinary.com" in raw_url and raw_url.endswith(".pdf")):
            doc["url"] = f"/api/resources/file/{rid}"
        for field in ("uploaded_at", "reviewed_at"):
            if isinstance(doc.get(field), datetime):
                doc[field] = format_iso(doc.get(field))
    return JSONResponse(
        content=docs,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )

from database import upload_file, get_file


@router.get("/playlists")
async def get_playlists_for_students(subject_id: Optional[str] = None):
    """
    Returns video course playlists for a subject (public student endpoint).
    Merges dynamic db.playlists, approved resource playlists, AND prebuilt seed playlists from db.subjects.
    """
    all_playlists = []
    seen_keys = set()  # (subject_id, url_or_title)

    clean_sub_id = subject_id.strip().upper() if subject_id and subject_id.strip() else None

    # 1. Fetch from db.playlists collection
    query1 = {}
    if clean_sub_id:
        query1["subject_id"] = {"$regex": f"^{re.escape(clean_sub_id)}$", "$options": "i"}

    cursor1 = db.playlists.find(query1).sort("created_at", -1)
    docs1 = await cursor1.to_list(length=None)
    for d in docs1:
        d.pop("_id", None)
        sub_code = d.get("subject_id", "").upper()
        url = d.get("url") or ""
        title = d.get("title") or ""
        key = (sub_code, (url.strip() or title.strip()).lower())
        if key not in seen_keys:
            seen_keys.add(key)
            d["source"] = d.get("source", "admin")
            # Extract real YouTube playlist or video ID
            list_m = re.search(r'[?&]list=([A-Za-z0-9_-]+)', url)
            if list_m:
                d["yt_list_id"] = list_m.group(1)
            vid_m = re.search(r'(?:v=|\/embed\/|\/watch\?v=|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})', url)
            if vid_m:
                d["yt_video_id"] = vid_m.group(1)
            for field in ("created_at", "updated_at"):
                if isinstance(d.get(field), datetime):
                    d[field] = format_iso(d.get(field))
            all_playlists.append(d)

    # 2. Fetch approved playlist resources from db.resources collection
    query2 = {"status": "approved", "resource_type": "playlist"}
    if clean_sub_id:
        query2["subject_id"] = {"$regex": f"^{re.escape(clean_sub_id)}$", "$options": "i"}

    cursor2 = db.resources.find(query2).sort("uploaded_at", -1)
    docs2 = await cursor2.to_list(length=None)
    for r in docs2:
        sub_code = r.get("subject_id", "").upper()
        url = r.get("url") or ""
        title = r.get("title") or ""
        key = (sub_code, (url.strip() or title.strip()).lower())
        if key not in seen_keys:
            seen_keys.add(key)
            match = re.search(r'list=([A-Za-z0-9_-]+)', url)
            playlist_id = match.group(1) if match else r.get("resource_id")
            uploaded_at_str = format_iso(r.get("uploaded_at")) if isinstance(r.get("uploaded_at"), datetime) else r.get("uploaded_at")
            all_playlists.append({
                "playlist_id": playlist_id,
                "subject_id": sub_code,
                "title": title,
                "url": url,
                "unit": "Community Playlist",
                "created_at": uploaded_at_str,
                "source": "community",
                "resource_id": r.get("resource_id")
            })

    # 3. Fetch prebuilt seed playlists from db.subjects collection
    query3 = {"playlists": {"$exists": True, "$ne": []}}
    if clean_sub_id:
        query3["code"] = {"$regex": f"^{re.escape(clean_sub_id)}$", "$options": "i"}

    cursor3 = db.subjects.find(query3)
    subj_docs = await cursor3.to_list(length=None)
    for subj in subj_docs:
        sub_code = subj.get("code", "").upper()
        subj_name = subj.get("name", sub_code)
        for idx, item in enumerate(subj.get("playlists", [])):
            if isinstance(item, dict):
                title = item.get("title") or f"{subj_name} - {item.get('channel', 'Lectures')}"
                url = item.get("url") or ""
                unit = item.get("channel") or "Full Course"
            elif isinstance(item, str):
                title = f"{subj_name} Course Playlist"
                url = item
                unit = "Full Course"
            else:
                continue

            key = (sub_code, (url.strip() or title.strip()).lower())
            if key not in seen_keys and url:
                seen_keys.add(key)
                match = re.search(r'list=([A-Za-z0-9_-]+)', url)
                playlist_id = match.group(1) if match else f"seed-{sub_code}-{idx}"
                all_playlists.append({
                    "playlist_id": playlist_id,
                    "subject_id": sub_code,
                    "title": title,
                    "url": url,
                    "unit": unit,
                    "created_at": None,
                    "source": "seed"
                })

    return JSONResponse(
        content=all_playlists,
        headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    )

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
    Resolves internal MongoDB playlist_ids, UUIDs, and single video links dynamically.
    """
    if not list_id or not list_id.strip():
        raise HTTPException(status_code=400, detail="list_id is required.")

    raw_id = list_id.strip()
    clean_list_id = raw_id
    single_video_id = None
    target_title = None

    # 1. Direct URL extraction if query passed as full URL
    if "list=" in clean_list_id:
        m = re.search(r'[?&]list=([A-Za-z0-9_-]+)', clean_list_id)
        if m:
            clean_list_id = m.group(1)

    # 2. Database lookup if clean_list_id is a UUID or DB resource key
    is_uuid = bool(re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', clean_list_id, re.IGNORECASE))
    if is_uuid or clean_list_id.startswith("seed-") or not (clean_list_id.startswith("PL") or clean_list_id.startswith("UU") or clean_list_id.startswith("FL") or clean_list_id.startswith("RD") or clean_list_id.startswith("OLAK")):
        doc = await db.playlists.find_one({"$or": [{"playlist_id": clean_list_id}, {"resource_id": clean_list_id}]})
        if not doc:
            doc = await db.resources.find_one({"$or": [{"resource_id": clean_list_id}, {"playlist_id": clean_list_id}]})
        
        if doc:
            target_title = doc.get("title")
            doc_url = doc.get("url") or ""
            if doc_url:
                list_m = re.search(r'[?&]list=([A-Za-z0-9_-]+)', doc_url)
                if list_m:
                    clean_list_id = list_m.group(1)
                else:
                    vid_m = re.search(r'(?:v=|\/embed\/|\/watch\?v=|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})', doc_url)
                    if vid_m:
                        single_video_id = vid_m.group(1)

    # 3. Handle single video link
    if single_video_id:
        single_item = [{
            "videoId": single_video_id,
            "title": target_title or "Lecture Video",
            "index": 1,
            "thumbnail": f"https://img.youtube.com/vi/{single_video_id}/hqdefault.jpg"
        }]
        return {
            "list_id": clean_list_id,
            "total_videos": 1,
            "videos": single_item
        }

    # Handle direct single 11-char video ID input
    vid_direct_m = re.search(r'(?:v=|\/embed\/|\/watch\?v=|\/v\/|youtu\.be\/|^)([A-Za-z0-9_-]{11})$', clean_list_id)
    if vid_direct_m and not (clean_list_id.startswith("PL") or clean_list_id.startswith("UU") or clean_list_id.startswith("FL") or clean_list_id.startswith("RD") or clean_list_id.startswith("OLAK")):
        v_id = vid_direct_m.group(1)
        single_item = [{
            "videoId": v_id,
            "title": target_title or "Lecture Video",
            "index": 1,
            "thumbnail": f"https://img.youtube.com/vi/{v_id}/hqdefault.jpg"
        }]
        return {
            "list_id": v_id,
            "total_videos": 1,
            "videos": single_item
        }

    videos = fetch_youtube_playlist_videos(clean_list_id)

    # Fallback: If 0 videos found and URL has a video ID, return single video item
    if not videos and doc_url if 'doc_url' in locals() else False:
        m_v = re.search(r'(?:v=|\/watch\?v=|\/embed\/|youtu\.be\/)([A-Za-z0-9_-]{11})', doc_url)
        if m_v:
            videos = [{
                "videoId": m_v.group(1),
                "title": target_title or "Lecture Video",
                "index": 1,
                "thumbnail": f"https://img.youtube.com/vi/{m_v.group(1)}/hqdefault.jpg"
            }]

    return {
        "list_id": clean_list_id,
        "total_videos": len(videos),
        "videos": videos
    }


@router.get("/file/{resource_id}")
async def stream_resource_file(resource_id: str):
    """
    Streams PDF file directly from MongoDB GridFS, cached bytes, or Cloudinary proxy with inline headers.
    """
    query = {
        "$or": [
            {"resource_id": resource_id},
            {"cloud_file_id": resource_id},
            {"cloudinary_public_id": resource_id}
        ]
    }
    try:
        from bson import ObjectId
        if ObjectId.is_valid(resource_id):
            oid = ObjectId(resource_id)
            query["$or"].extend([{"_id": oid}, {"cloud_file_id": oid}])
    except Exception:
        pass

    doc = await db.resources.find_one(query)
    
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
        filename = file.filename or "student_submission.pdf"
        ext = filename.split(".")[-1].lower() if "." in filename else ""

        # ── Step 1: PDF Compression Pipeline ──────────────────────────────────
        if ext == "pdf" or file.content_type == "application/pdf":
            content_bytes = compress_pdf_bytes(content_bytes, target_max_bytes=MAX_FILE_SIZE)

        if len(content_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File ({len(content_bytes) / (1024 * 1024):.1f} MB) exceeds the 10 MB student upload limit even after compression.")

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


# ── In-Place PDF Chat & PDF Quiz Generator Endpoints ─────────────────────────

from urllib.parse import urlparse

ALLOWED_PDF_DOMAINS = {
    "res.cloudinary.com",
    "cloudinary.com",
    "edumind-ebk1.onrender.com",
    "edumind-five.vercel.app",
    "localhost",
    "127.0.0.1"
}

def _is_trusted_pdf_url(url: str) -> bool:
    """Verifies that remote HTTP requests target trusted Cloudinary CDN, internal domains, or private network IPs."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        hostname = (parsed.hostname or "").lower()
        if not hostname:
            return False
        if "cloudinary" in hostname or "onrender.com" in hostname or "vercel.app" in hostname:
            return True
        if hostname in ("localhost", "127.0.0.1") or hostname.startswith("192.168.") or hostname.startswith("10.") or hostname.startswith("172."):
            return True
        return any(hostname == d or hostname.endswith("." + d) for d in ALLOWED_PDF_DOMAINS)
    except Exception:
        return False


class PdfChatPayload(BaseModel):
    pdf_url: Optional[str] = None
    resource_id: Optional[str] = None
    message: str
    history: Optional[List[dict]] = []

class SingleQuizQuestion(BaseModel):
    id: int
    page: int
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class PdfQuizPayload(BaseModel):
    pdf_url: Optional[str] = None
    resource_id: Optional[str] = None
    title: Optional[str] = None


async def _fetch_pdf_bytes_and_text(pdf_url: Optional[str], resource_id: Optional[str]):
    """
    Retrieves PDF bytes strictly for approved resources, extracts text page-by-page,
    and returns content_bytes, page_count, page_texts, full_pdf_text, and has_readable_text flag.
    Employs multi-pass PyMuPDF extraction, native pypdf fallback, and Multimodal Vision OCR.
    """
    content_bytes = None

    # 1. Direct GridFS / DB lookup if resource_id provided or embedded in URL
    if not resource_id and pdf_url:
        match = re.search(r'/file/([A-Za-z0-9_-]+)', str(pdf_url))
        if match:
            resource_id = match.group(1)
        else:
            q_match = re.search(r'[?&](?:resource_id|file_id|id)=([A-Za-z0-9_-]+)', str(pdf_url))
            if q_match:
                resource_id = q_match.group(1)

    if resource_id:
        query = {
            "$or": [
                {"resource_id": resource_id},
                {"cloud_file_id": resource_id},
                {"cloudinary_public_id": resource_id}
            ]
        }
        try:
            from bson import ObjectId
            if ObjectId.is_valid(resource_id):
                oid = ObjectId(resource_id)
                query["$or"].extend([{"_id": oid}, {"cloud_file_id": oid}])
        except Exception:
            pass

        doc = await db.resources.find_one(query)
        
        # Access Scope Guard: Only approved resources can be accessed for interactive AI chat/quiz
        if doc and doc.get("status") != "approved":
            raise HTTPException(
                status_code=403,
                detail="Access denied: Only approved resources can be accessed for interactive PDF chat or quiz generation."
            )

        if doc and doc.get("file_bytes_cache") and len(doc.get("file_bytes_cache")) > 0:
            content_bytes = doc.get("file_bytes_cache")
        elif doc and doc.get("cloud_file_id"):
            file_obj = await get_file(str(doc.get("cloud_file_id")))
            if file_obj and file_obj.get("content") and len(file_obj["content"]) > 0:
                content_bytes = file_obj["content"]
        
        if not content_bytes:
            file_obj = await get_file(resource_id)
            if file_obj and file_obj.get("content") and len(file_obj["content"]) > 0:
                content_bytes = file_obj["content"]

        if not content_bytes and doc:
            ext_url = doc.get("url") or doc.get("cloudinary_url")
            if ext_url and str(ext_url).startswith("http"):
                if not _is_trusted_pdf_url(ext_url):
                    logger.warning(f"Blocked untrusted resource URL fetch: {ext_url}")
                else:
                    try:
                        resp = requests.get(ext_url, timeout=20)
                        if resp.status_code == 200 and resp.content and len(resp.content) > 0:
                            content_bytes = resp.content
                    except Exception as e:
                        logger.warning(f"Failed to fetch trusted resource URL {ext_url}: {e}")

        # Fallback: Check GridFS by filename if metadata exists
        if not content_bytes and doc and (doc.get("filename") or doc.get("title")):
            try:
                from database import get_fs
                bucket = get_fs()
                candidates = [doc.get("filename"), f"{doc.get('title')}.pdf", doc.get("title")]
                for cand in candidates:
                    if not cand: continue
                    try:
                        grid_out = await bucket.open_download_stream_by_name(cand)
                        data = await grid_out.read()
                        if data and len(data) > 0:
                            content_bytes = data
                            break
                    except Exception:
                        pass
            except Exception:
                pass

    # 2. External HTTP download fallback (SSRF-protected)
    if not content_bytes and pdf_url and str(pdf_url).startswith("http"):
        if not _is_trusted_pdf_url(pdf_url):
            logger.warning(f"Blocked untrusted external PDF URL fetch attempt: {pdf_url}")
            raise HTTPException(status_code=400, detail="Invalid PDF URL: Untrusted domain rejected.")
        try:
            resp = requests.get(pdf_url, timeout=20)
            if resp.status_code == 200 and resp.content and len(resp.content) > 0:
                content_bytes = resp.content
        except Exception as e:
            logger.warning(f"Failed to fetch pdf_url {pdf_url}: {e}")

    if not content_bytes:
        raise HTTPException(status_code=404, detail="Could not retrieve PDF file content.")

    # 3. Extract text page-by-page using PyMuPDF / fitz with multi-pass extraction
    page_texts = []
    page_count = 1
    try:
        import fitz
        doc = fitz.open(stream=content_bytes, filetype="pdf")
        if getattr(doc, "is_encrypted", False) or getattr(doc, "needs_pass", False):
            try: doc.authenticate("")
            except Exception: pass
        
        page_count = max(1, len(doc))
        for i, page in enumerate(doc):
            t = ""
            # Pass 1: Standard plain text
            try:
                t = (page.get_text("text") or "").strip()
            except Exception:
                pass

            # Pass 2: Text blocks fallback
            if not t:
                try:
                    blocks = page.get_text("blocks")
                    if blocks:
                        t = "\n".join([b[4] for b in blocks if len(b) >= 5 and isinstance(b[4], str) and b[4].strip()]).strip()
                except Exception:
                    pass

            # Pass 3: Words sequence fallback
            if not t:
                try:
                    words = page.get_text("words")
                    if words:
                        t = " ".join([w[4] for w in words if len(w) >= 5 and isinstance(w[4], str) and w[4].strip()]).strip()
                except Exception:
                    pass

            # Pass 4: Layout / rawtext fallback
            if not t:
                try:
                    t = (page.get_text("layout") or page.get_text("rawtext") or "").strip()
                except Exception:
                    pass

            # Pass 5: Field widgets / form values
            if not t:
                try:
                    widget_texts = [w.field_value for w in page.widgets() if getattr(w, 'field_value', None)]
                    if widget_texts:
                        t = "\n".join([str(wt).strip() for wt in widget_texts if str(wt).strip()]).strip()
                except Exception:
                    pass

            if not t:
                t = f"[Scanned/Diagram Content on Page {i+1}]"
            
            page_texts.append(f"--- Page {i+1} ---\n{t}")
        doc.close()
    except Exception as e:
        logger.warning(f"PyMuPDF parse error: {e}")
        from rag.ingester import extract_text_from_pdf
        full_extracted = extract_text_from_pdf(content_bytes, "document.pdf")
        page_texts = [full_extracted]
        page_count = 1

    full_pdf_text = "\n\n".join(page_texts)

    # 4. Guardrail check for readable text layer vs scanned/empty document
    cleaned_probe = re.sub(r'--- Page \d+ ---|\[Scanned/Diagram Content on Page \d+\]', '', full_pdf_text).strip()
    
    # If text is too sparse (< 50 chars), trigger full multi-engine ingester fallback (pypdf + Vision OCR)
    if len(cleaned_probe) < 50:
        logger.info("PDF has sparse text layer (<50 chars). Running secondary multi-engine ingester fallback...")
        try:
            from rag.ingester import extract_text_from_pdf
            secondary_text = extract_text_from_pdf(content_bytes, "document.pdf")
            if secondary_text and len(secondary_text.strip()) > len(cleaned_probe):
                full_pdf_text = secondary_text
                cleaned_probe = re.sub(r'--- Page \d+ ---|\[Scanned/Diagram Content on Page \d+\]', '', full_pdf_text).strip()
                # If secondary has page splits, use them
                if "--- Page " in full_pdf_text:
                    page_texts = [p.strip() for p in full_pdf_text.split("--- Page ") if p.strip()]
                    page_texts = [f"--- Page {p}" for p in page_texts]
                    page_count = max(1, len(page_texts))
                else:
                    page_texts = [full_pdf_text]
        except Exception as fallback_err:
            logger.warning(f"Secondary text extraction notice: {fallback_err}")

    # If STILL sparse (< 50 chars), attempt direct Multimodal Vision OCR on first 10 pages
    if len(cleaned_probe) < 50:
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        if gemini_key or openai_key:
            logger.info("Running direct Multimodal Vision OCR on scanned PDF pages...")
            try:
                import fitz
                import base64
                doc = fitz.open(stream=content_bytes, filetype="pdf")
                ocr_page_texts = []
                for p_idx in range(min(10, len(doc))):
                    try:
                        page = doc[p_idx]
                        pix = page.get_pixmap(dpi=150)
                        img_b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")
                        ocr_txt = ""
                        if gemini_key:
                            try:
                                from langchain_google_genai import ChatGoogleGenerativeAI
                                from langchain_core.messages import HumanMessage
                                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_key)
                                res = llm.invoke([HumanMessage(content=[
                                    {"type": "text", "text": "Extract all readable academic text, formulas, headings, and bullet points from this document page verbatim."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                                ])])
                                if res and res.content:
                                    ocr_txt = str(res.content).strip()
                            except Exception as g_err:
                                logger.warning(f"Direct Gemini Vision OCR notice for page {p_idx+1}: {g_err}")

                        if not ocr_txt and openai_key:
                            try:
                                from langchain_openai import ChatOpenAI
                                from langchain_core.messages import HumanMessage
                                llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
                                res = llm.invoke([HumanMessage(content=[
                                    {"type": "text", "text": "Extract all readable academic text, formulas, headings, and bullet points from this document page verbatim."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                                ])])
                                if res and res.content:
                                    ocr_txt = str(res.content).strip()
                            except Exception as o_err:
                                logger.warning(f"Direct OpenAI Vision OCR notice for page {p_idx+1}: {o_err}")

                        if ocr_txt:
                            ocr_page_texts.append(f"--- Page {p_idx+1} ---\n{ocr_txt}")
                    except Exception:
                        continue
                doc.close()
                if ocr_page_texts:
                    page_texts = ocr_page_texts
                    full_pdf_text = "\n\n".join(page_texts)
                    cleaned_probe = re.sub(r'--- Page \d+ ---|\[Scanned/Diagram Content on Page \d+\]', '', full_pdf_text).strip()
            except Exception as ocr_exc:
                logger.warning(f"Direct Multimodal Vision OCR exception: {ocr_exc}")

    # Set has_readable_text flag with relaxed threshold (>=15 characters)
    has_readable_text = len(cleaned_probe) >= 15

    return content_bytes, page_count, page_texts, full_pdf_text, has_readable_text


@router.post("/pdf-chat")
@limiter.limit("10/minute")
async def chat_with_pdf(request: Request, payload: PdfChatPayload):
    """Interactive in-place Chat with PDF content (Rate-limited, status-guarded)."""
    if not payload.message or not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message is required.")

    _, page_count, _, full_text, has_readable_text = await _fetch_pdf_bytes_and_text(payload.pdf_url, payload.resource_id)
    
    # Refusal Guard: Do not hallucinate on scanned or empty documents
    if not has_readable_text:
        return {
            "reply": "⚠️ No readable text layer was detected in this document (it appears to be a scanned image or empty). Please upload an OCR-processed or text-based PDF to chat with AI.",
            "page_count": page_count
        }

    truncated_text = full_text[:60000]

    history_str = ""
    if payload.history:
        history_parts = []
        for h in payload.history[-6:]:
            role = "Student" if h.get("role") == "user" else "AI Tutor"
            history_parts.append(f"{role}: {h.get('content')}")
        history_str = "\n".join(history_parts)

    prompt = f"""You are EduMind AI PDF Tutor, an expert academic assistant explaining a course document ({page_count} Pages total).

=== ATTACHED PDF DOCUMENT CONTENT ===
{truncated_text}
======================================

Recent Conversation Context:
{history_str}

Student Question: "{payload.message}"

INSTRUCTIONS:
1. Provide a comprehensive, easy-to-understand explanation specifically based on the PDF contents above.
2. If the user asks to explain a concept, break it down clearly step-by-step with simple analogies or examples.
3. Cite page numbers (e.g. "According to Page 2...") whenever applicable.
4. Format your output nicely using markdown bolding, bullet points, and code blocks if relevant.
"""

    from rag.generator import generate_with_retry
    reply = generate_with_retry(prompt)
    if not reply:
        reply = "I was unable to analyze this document right now. Please try again or ask a more specific question."
    return {
        "reply": reply,
        "page_count": page_count
    }


@router.post("/pdf-quiz")
@limiter.limit("5/minute")
async def generate_pdf_quiz(request: Request, payload: PdfQuizPayload):
    """Generates an in-place interactive quiz strictly based on PDF content with Pydantic schema validation."""
    _, page_count, _, full_text, has_readable_text = await _fetch_pdf_bytes_and_text(payload.pdf_url, payload.resource_id)
    
    # Refusal Guard: Refuse scanned documents lacking readable text
    if not has_readable_text:
        raise HTTPException(
            status_code=422,
            detail="Cannot generate quiz: This document contains only scanned diagrams or images without readable text. Please use an OCR-processed or text-based PDF."
        )

    # Requirement: Number of questions = 2 * number of pages that PDF contains (between 2 and 50)
    target_questions = max(2, min(50, page_count * 2))
    truncated_text = full_text[:60000]

    prompt = f"""You are an expert university exam question creator.
Analyze the following course PDF document ({page_count} Pages total) and generate EXACTLY {target_questions} multiple-choice questions strictly based on the content.

=== PDF DOCUMENT CONTENT ({page_count} Pages) ===
{truncated_text}
======================================

STRICT REQUIREMENTS:
1. You MUST generate EXACTLY {target_questions} questions (which is 2 questions for each of the {page_count} pages).
2. Every question MUST be directly factual and answerable from the PDF text.
3. Include 4 distinct options (A, B, C, D) for each question.
4. Provide a clear detailed explanation citing the exact Page number.
5. Return ONLY a valid JSON object matching this schema (NO MARKDOWN WRAPPERS, NO EXTRA PROSE):

{{
  "pdf_title": "{payload.title or 'Course PDF'}",
  "page_count": {page_count},
  "total_questions": {target_questions},
  "questions": [
    {{
      "id": 1,
      "page": 1,
      "question": "What is the primary characteristic of a block cipher?",
      "options": [
        "A) Encrypts streams byte by byte",
        "B) Encrypts a single block of a fixed size (n bits)",
        "C) Hashes input string to fixed length",
        "D) Uses asymmetric public keys"
      ],
      "correct_answer": 1,
      "explanation": "According to Page 1, a block cipher can encrypt a single block of a fixed size (n bits)."
    }}
  ]
}}
"""

    from rag.generator import generate_with_retry
    raw_res = generate_with_retry(prompt)
    if not raw_res:
        raise HTTPException(status_code=500, detail="Failed to generate quiz from AI model. Please try again.")
    
    try:
        # Robust regex-based JSON block extraction (handles markdown preambles or raw json)
        json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', raw_res)
        if json_match:
            json_str = json_match.group(1)
        else:
            bracket_match = re.search(r'(\{[\s\S]*\})', raw_res)
            json_str = bracket_match.group(1) if bracket_match else raw_res

        quiz_data = json.loads(json_str.strip())

        # Validate schema parity
        questions_raw = quiz_data.get("questions", [])
        validated_questions = []
        for idx, q in enumerate(questions_raw):
            try:
                opts = q.get("options", [])
                if len(opts) < 4:
                    opts = opts + [f"Option {chr(65 + i)}" for i in range(len(opts), 4)]
                validated_questions.append({
                    "id": int(q.get("id", idx + 1)),
                    "page": int(q.get("page", 1)),
                    "question": str(q.get("question", f"Question {idx+1}")),
                    "options": [str(o) for o in opts[:4]],
                    "correct_answer": int(q.get("correct_answer", 0)) % 4,
                    "explanation": str(q.get("explanation", "Refer to document text for explanation."))
                })
            except Exception:
                continue

        if not validated_questions:
            raise ValueError("No questions satisfied validation.")

        return {
            "pdf_title": quiz_data.get("pdf_title", payload.title or "Course PDF"),
            "page_count": page_count,
            "total_questions": len(validated_questions),
            "questions": validated_questions
        }
    except Exception as parse_err:
        logger.warning(f"Failed to parse or validate quiz JSON: {parse_err}. Raw response: {raw_res[:200]}")
        raise HTTPException(status_code=500, detail="Failed to parse valid quiz JSON from AI model. Please try again.")
