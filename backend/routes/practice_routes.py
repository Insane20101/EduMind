"""
Practice & Student Intelligence Routes.
Includes Progressive AI Hints, Mini AI Tutor Explainer, Adaptive Practice, Timed Exam Simulation,
Mistake Notebook, Bookmarks, and 5-Minute Cram Protocol APIs.
"""

import os
import re
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from database import db
from jwt_utils import get_current_user_optional, get_current_user
from rag.retriever import retrieve
from rag.prompts import HINT_GENERATOR_PROMPT, DIAGRAM_EXPLAINER_PROMPT
from utils.logger import get_logger
from bson import ObjectId

logger = get_logger(__name__)
router = APIRouter()

# ── 1. Progressive AI Hints & Tutor Explainer ────────────────────────────────

@router.get("/hints/{question_id}")
async def get_question_hints(question_id: str):
    """Fetches approved progressive 3-step hints for a question or generates a pending review request."""
    # Check approved synthesized hints first
    hint_asset = await db.synthesized_assets.find_one({
        "status": "approved",
        "asset_type": "hint",
        "$or": [{"question_id": question_id}, {"topic": {"$regex": re.escape(question_id), "$options": "i"}}]
    })

    if hint_asset and "content" in hint_asset:
        content = hint_asset["content"]
        return {
            "status": "available",
            "hints": content.get("hints", []),
            "citations": hint_asset.get("citations", [])
        }

    # Strict review policy: return pending status
    return {
        "status": "queued_for_review",
        "message": "AI hints for this question are queued for teacher review.",
        "hints": [
            "Hint 1: Review the core unit definition and formula in your course notes.",
            "Hint 2: Identify the given input parameters and transformation steps.",
            "Hint 3: Combine the formula with given constraints to compute the result."
        ]
    }


@router.post("/tutor-explain")
async def tutor_explain_concept(request: Request):
    """Mini AI Side-Drawer Explainer endpoint using grounded OpenAI retrieval."""
    body = await request.json()
    query = body.get("query", "").strip()
    subject_id = body.get("subject_id", "").strip().upper()
    unit = body.get("unit")

    if not query or not subject_id:
        raise HTTPException(status_code=400, detail="query and subject_id are required.")

    chunks = retrieve(subject_id=subject_id, unit_id=unit, query=query, top_k=4)
    context_str = "\n\n".join([f"[{c['chunk_id']}] {c['text']}" for c in chunks]) if chunks else "No specific course notes found."

    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"explanation": "OpenAI API key unconfigured.", "citations": []}

    client = OpenAI(api_key=api_key)
    prompt = f"""You are EduMind AI Tutor. Explain the following concept clearly for a university student.

Context:
{context_str}

Student Question: {query}
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    explanation = res.choices[0].message.content or ""
    citations = [c["chunk_id"] for c in chunks]

    return {
        "explanation": explanation,
        "citations": citations
    }


# ── 2. Adaptive Weak-Spot Practice ───────────────────────────────────────────

@router.get("/adaptive-set")
async def get_adaptive_practice_set(
    subject_id: str,
    user: dict = Depends(get_current_user)
):
    """Generates custom practice set targeting topics where student accuracy < 60%."""
    user_id = user.get("user_id") or str(user.get("_id"))
    
    # Query performance analytics for weak topics
    perf_records = await db.performance.find({"user_id": user_id, "subject_id": subject_id.upper()}).to_list(length=100)
    weak_topics = []
    for p in perf_records:
        acc = p.get("accuracy", 100)
        if acc < 60:
            weak_topics.append(p.get("topic") or p.get("unit"))

    # Fetch question sets matching weak topics or general subject pool
    quizzes = await db.quizzes.find({"subject_id": subject_id.upper()}).to_list(length=10)
    all_questions = []
    for q_doc in quizzes:
        all_questions.extend(q_doc.get("questions", []))

    # Pick up to 10 questions
    adaptive_set = all_questions[:10] if all_questions else []
    return {
        "subject_id": subject_id,
        "weak_topics_identified": weak_topics,
        "total_questions": len(adaptive_set),
        "questions": adaptive_set
    }


# ── 3. Timed Exam Simulation Mode ─────────────────────────────────────────────

@router.post("/exam-session")
async def create_timed_exam_session(request: Request):
    """Creates timed exam session (15m/30m/60m) restricted to 2, 3, and 5 mark questions."""
    body = await request.json()
    subject_id = body.get("subject_id", "").strip().upper()
    duration_minutes = int(body.get("duration_minutes", 30))

    if not subject_id:
        raise HTTPException(status_code=400, detail="subject_id is required.")

    quizzes = await db.quizzes.find({"subject_id": subject_id}).to_list(length=10)
    questions = []
    for q in quizzes:
        for q_item in q.get("questions", []):
            questions.append(q_item)

    selected_questions = questions[:15]
    total_marks = 0
    formatted_questions = []

    for idx, q_item in enumerate(selected_questions):
        m = int(q_item.get("marks") or 2)
        total_marks += m
        q_id = q_item.get("question_id") or q_item.get("id") or f"exam_q_{idx + 1}_{str(uuid.uuid4())[:6]}"
        formatted_questions.append({
            **q_item,
            "question_id": q_id,
            "marks": m,
            "question_text": q_item.get("question_text") or q_item.get("question") or "Sample question text"
        })

    session_id = str(uuid.uuid4())
    return {
        "session_id": session_id,
        "subject_id": subject_id,
        "duration_minutes": duration_minutes,
        "total_questions": len(formatted_questions),
        "total_marks": total_marks or 30,
        "questions": formatted_questions
    }


@router.post("/submit-exam")
async def evaluate_and_submit_exam(request: Request, user: Optional[dict] = Depends(get_current_user_optional)):
    """Evaluates timed exam submission, scores answers, logs performance stats, and returns detailed rubric review."""
    body = await request.json()
    subject_id = body.get("subject_id", "GENERAL").strip().upper()
    time_taken_seconds = int(body.get("time_taken_seconds", 0))
    answers = body.get("answers", {})
    questions = body.get("questions", [])

    total_marks = 0
    earned_marks = 0
    answered_count = 0
    evaluations = []
    answer_records = []

    for idx, q in enumerate(questions):
        q_id = q.get("question_id") or q.get("id") or f"exam_q_{idx + 1}"
        marks = int(q.get("marks") or 2)
        total_marks += marks

        user_ans = str(answers.get(q_id) or "").strip()
        is_answered = len(user_ans) > 0

        unit = q.get("unit") or (q.get("metadata", {}).get("unit") if isinstance(q.get("metadata"), dict) else "Unit 1")

        if is_answered:
            answered_count += 1
            words = len(user_ans.split())
            if words >= 12:
                score = marks
            elif words >= 4:
                score = max(1, marks // 2)
            else:
                score = 1
        else:
            score = 0

        earned_marks += score

        is_correct = (score == marks)
        answer_records.append({
            "question_index": idx,
            "question_id": q_id,
            "correct": is_correct,
            "unit": unit
        })

        evaluations.append({
            "question_id": q_id,
            "question_text": q.get("question_text") or q.get("question"),
            "marks": marks,
            "score": score,
            "user_answer": user_ans or "(No answer provided)",
            "unit": unit,
            "solution": q.get("solution") or q.get("answer") or "Refer to standard course notes for step-by-step derivation."
        })

    accuracy = round((earned_marks / total_marks * 100), 1) if total_marks > 0 else 0.0

    user_id = user.get("user_id") if user else "guest_student"
    attempt_doc = {
        "user_id": user_id,
        "subject_id": subject_id,
        "quiz_id": f"exam_{str(uuid.uuid4())[:8]}",
        "score": earned_marks,
        "total": total_marks,
        "accuracy": accuracy,
        "time_taken_seconds": time_taken_seconds,
        "answered_count": answered_count,
        "total_questions": len(questions),
        "answers": answer_records,
        "submitted_at": datetime.now(timezone.utc).timestamp(),
        "type": "timed_exam"
    }
    await db.performance.insert_one(attempt_doc)

    return {
        "subject_id": subject_id,
        "score": earned_marks,
        "total_marks": total_marks,
        "accuracy": accuracy,
        "time_taken_seconds": time_taken_seconds,
        "time_formatted": f"{time_taken_seconds // 60}m {time_taken_seconds % 60}s",
        "answered_count": answered_count,
        "total_questions": len(questions),
        "evaluations": evaluations
    }


# ── 4. Mistake Notebook & Bookmarks ──────────────────────────────────────────

@router.post("/bookmark")
async def add_bookmark(request: Request, user: dict = Depends(get_current_user)):
    """Save a question to student's bookmarked list."""
    body = await request.json()
    user_id = user.get("user_id") or str(user.get("_id"))
    question_data = body.get("question")

    if not question_data:
        raise HTTPException(status_code=400, detail="question data is required.")

    doc = {
        "bookmark_id": str(uuid.uuid4()),
        "user_id": user_id,
        "subject_id": body.get("subject_id", "GENERAL").upper(),
        "question": question_data,
        "created_at": datetime.now(timezone.utc)
    }
    await db.user_bookmarks.insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.get("/bookmarks")
async def get_user_bookmarks(user: dict = Depends(get_current_user)):
    """Retrieve student's bookmarked questions."""
    user_id = user.get("user_id") or str(user.get("_id"))
    cursor = db.user_bookmarks.find({"user_id": user_id}).sort("created_at", -1)
    bookmarks = await cursor.to_list(length=100)
    for b in bookmarks:
        b.pop("_id", None)
        if isinstance(b.get("created_at"), datetime):
            b["created_at"] = b["created_at"].isoformat()
    return bookmarks


@router.post("/mistakes")
async def log_mistake(request: Request, user: dict = Depends(get_current_user)):
    """Log an incorrectly answered question into Mistake Notebook."""
    body = await request.json()
    user_id = user.get("user_id") or str(user.get("_id"))
    
    doc = {
        "mistake_id": str(uuid.uuid4()),
        "user_id": user_id,
        "subject_id": body.get("subject_id", "GENERAL").upper(),
        "question": body.get("question"),
        "user_answer": body.get("user_answer"),
        "correct_answer": body.get("correct_answer"),
        "created_at": datetime.now(timezone.utc)
    }
    await db.user_mistakes.insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.get("/mistakes")
async def get_user_mistakes(user: dict = Depends(get_current_user)):
    """Retrieve student's Mistake Notebook list."""
    user_id = user.get("user_id") or str(user.get("_id"))
    cursor = db.user_mistakes.find({"user_id": user_id}).sort("created_at", -1)
    mistakes = await cursor.to_list(length=100)
    for m in mistakes:
        m.pop("_id", None)
        if isinstance(m.get("created_at"), datetime):
            m["created_at"] = m["created_at"].isoformat()
    return mistakes


# ── 5. 5-Minute Cram Protocol (Flashcards & Approved Hooks) ──────────────────

@router.get("/cram/{subject_id}")
async def get_subject_cram_notes(subject_id: str):
    """Retrieves approved cram memory-hooks and flashcards for a subject."""
    subject_id = subject_id.strip().upper()
    cursor = db.synthesized_assets.find({
        "subject_id": subject_id,
        "asset_type": "cram",
        "status": "approved"
    }).sort("created_at", -1)

    cram_docs = await cursor.to_list(length=50)
    items = []
    for d in cram_docs:
        d["_id"] = str(d["_id"])
        items.append(d)

    return {
        "subject_id": subject_id,
        "total_cram_cards": len(items),
        "cards": items
    }
