from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from auth import router as auth_router
from database import init_db, db
from seed_subjects import seed_subjects_if_needed
from subjects import router as subjects_router
from routes.chat import router as chat_router
from routes.practice import router as practice_router
from routes.quiz import quiz_router
from routes.performance import performance_router
from routes.resources import router as resources_router
from routes.student_resources import router as student_resources_router

from limiter import limiter

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
import asyncio
import logging
from datetime import datetime
import httpx

from rag.vector_store import get_qdrant_client

logger = logging.getLogger(__name__)

async def keep_alive_pinger():
    url = os.getenv("RENDER_EXTERNAL_URL")
    if not url:
        logger.info("[KEEP-ALIVE] RENDER_EXTERNAL_URL not set; skipping keep-alive pinger loop.")
        return
    
    clean_url = url.rstrip('/')
    keep_alive_url = f"{clean_url}/api/keep-alive"
    logger.info(f"[KEEP-ALIVE] Starting self-pinging background task for {keep_alive_url}")
    
    await asyncio.sleep(60)
    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.get(keep_alive_url, timeout=10.0)
                logger.info(f"[KEEP-ALIVE] Ping to {keep_alive_url} returned status {resp.status_code}")
            except Exception as e:
                logger.warning(f"[KEEP-ALIVE] Ping failed: {e}")
            await asyncio.sleep(300) # Ping every 5 minutes

@app.on_event("startup")
async def startup_db_client():
    await init_db()
    await seed_subjects_if_needed(db)
    # Fail loud if QDRANT_URL or QDRANT_API_KEY is not configured
    get_qdrant_client()
    asyncio.create_task(keep_alive_pinger())

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
from routes.admin_auth import router as admin_auth_router
app.include_router(admin_auth_router, prefix="/api/admin/auth", tags=["admin_auth"])
app.include_router(resources_router, prefix="/api/admin/resources", tags=["admin-resources"])
app.include_router(student_resources_router, prefix="/api/resources", tags=["resources"])
app.include_router(subjects_router, prefix="/api/subjects", tags=["subjects"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(practice_router, tags=["practice"])
from routes.practice_routes import router as practice_intel_router
app.include_router(practice_intel_router, prefix="/api/practice", tags=["practice-intel"])
app.include_router(quiz_router, tags=["quiz"])
app.include_router(performance_router, tags=["performance"])


@app.get("/")
def root():
    return {"message": "EduMind API is running"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "EduMind API is warm"}

@app.get("/api/keep-alive")
def keep_alive():
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "EduMind-Backend"
    }

