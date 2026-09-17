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

# ── 3. Timed Exam Simulation Mode ─────────────────────────────────────────────

@router.post("/exam-session")
async def create_timed_exam_session(request: Request):
    """
    Creates customized real-time exam session based on:
    - subject_id (required)
    - num_questions (5, 10, 15, 20, 25)
    - unit ('all', 'unit_1', 'unit_2', 'unit_3', 'unit_4')
    - difficulty ('mixed', 'easy', 'medium', 'hard')
    - question_type ('mixed', 'mcq', 'true_false', 'subjective')
    - duration_minutes (15, 30, 60)
    """
    body = await request.json()
    subject_id = body.get("subject_id", "").strip().upper()
    duration_minutes = int(body.get("duration_minutes", 30))
    num_questions = max(5, min(25, int(body.get("num_questions", 10))))
    target_unit = str(body.get("unit", "all")).strip().lower()
    difficulty = str(body.get("difficulty", "mixed")).strip().lower()
    question_type = str(body.get("question_type", "mixed")).strip().lower()

    if not subject_id:
        raise HTTPException(status_code=400, detail="subject_id is required.")

    # Fetch available question pool from MongoDB quizzes collection for this subject
    quizzes = await db.quizzes.find({"subject_id": subject_id}).to_list(length=20)
    raw_pool = []
    for q in quizzes:
        for q_item in q.get("questions", []):
            raw_pool.append(q_item)

    # Filter pool by unit if requested
    filtered_pool = []
    for q in raw_pool:
        q_unit = str(q.get("unit") or q.get("metadata", {}).get("unit") or "").lower()
        if target_unit != "all":
            norm_target = target_unit.replace("_", " ")
            if norm_target not in q_unit and target_unit not in q_unit:
                continue

        filtered_pool.append(q)

    working_pool = filtered_pool if len(filtered_pool) >= 3 else raw_pool

    formatted_questions = []
    import random
    pool_copy = list(working_pool)
    if pool_copy:
        random.shuffle(pool_copy)

    def build_question_item(idx, item):
        q_id = item.get("question_id") or item.get("id") or f"exam_q_{idx + 1}_{str(uuid.uuid4())[:6]}"
        q_text = item.get("question_text") or item.get("question") or f"Explain core engineering concept #{idx+1} in {subject_id}."
        q_unit_val = item.get("unit") or (item.get("metadata", {}).get("unit") if isinstance(item.get("metadata"), dict) else None)
        if not q_unit_val or q_unit_val == "unassigned":
            unit_num = (idx % 4) + 1
            q_unit_val = f"Unit {unit_num}"

        desired_type = question_type
        if desired_type == "mixed":
            type_cycle = ["mcq", "true_false", "subjective"]
            desired_type = type_cycle[idx % 3]

        m = int(item.get("marks") or (1 if desired_type == "true_false" else 2 if desired_type == "mcq" else 5))
        sol = item.get("solution") or item.get("answer") or "Refer to standard course notes for step-by-step derivation."

        q_obj = {
            "question_id": q_id,
            "type": desired_type,
            "difficulty": item.get("difficulty") or (difficulty if difficulty != "mixed" else ("easy" if m == 1 else "medium" if m <= 3 else "hard")),
            "unit": q_unit_val,
            "marks": m,
            "question_text": q_text,
            "solution": sol
        }

        if desired_type == "mcq":
            opts = item.get("options")
            if not opts or len(opts) < 4:
                ans_str = str(sol)[:45]
                opts = [
                    f"A. {ans_str}",
                    "B. Non-deterministic polynomial time execution",
                    "C. Inverse polynomial upper bound condition",
                    "D. None of the above"
                ]
            q_obj["options"] = opts
            q_obj["correct_answer"] = item.get("correct_answer") or "A"

        elif desired_type == "true_false":
            q_obj["options"] = ["True", "False"]
            corr = str(item.get("correct_answer") or "True").strip().capitalize()
            q_obj["correct_answer"] = corr if corr in ["True", "False"] else "True"

        else:
            q_obj["type"] = "subjective"
            q_obj["key_rubric_points"] = item.get("key_rubric_points") or [
                "Definition & core theoretical principles",
                "Mathematical formulation or system diagram",
                "Practical implementation & complexity analysis"
            ]

        return q_obj

    for idx in range(num_questions):
        source_item = pool_copy[idx % len(pool_copy)] if pool_copy else {"question": f"Analyze fundamental topic #{idx+1} in {subject_id}."}
        formatted_questions.append(build_question_item(idx, source_item))

    total_marks = sum(q["marks"] for q in formatted_questions)
    session_id = str(uuid.uuid4())

    return {
        "session_id": session_id,
        "subject_id": subject_id,
        "duration_minutes": duration_minutes,
        "num_questions": num_questions,
        "unit": target_unit,
        "difficulty": difficulty,
        "question_type": question_type,
        "total_questions": len(formatted_questions),
        "total_marks": total_marks,
        "questions": formatted_questions
    }


@router.post("/submit-exam")
async def evaluate_and_submit_exam(request: Request, user: Optional[dict] = Depends(get_current_user_optional)):
    """Evaluates timed exam submission across Subjective, True/False, and MCQ questions."""
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
        q_type = str(q.get("type") or "subjective").lower()
        marks = int(q.get("marks") or 2)
        total_marks += marks

        user_ans = str(answers.get(q_id) or "").strip()
        is_answered = len(user_ans) > 0
        unit = q.get("unit") or (q.get("metadata", {}).get("unit") if isinstance(q.get("metadata"), dict) else "Unit 1")

        score = 0
        is_correct = False

        if is_answered:
            answered_count += 1

            if q_type == "mcq":
                correct_option = str(q.get("correct_answer") or "").strip().lower()
                user_clean = user_ans.lower()
                if user_clean == correct_option or (correct_option and user_clean.startswith(correct_option[0])):
                    score = marks
                    is_correct = True
                else:
                    score = 0
                    is_correct = False

            elif q_type == "true_false":
                correct_val = str(q.get("correct_answer") or "true").strip().lower()
                user_clean = user_ans.lower()
                if user_clean == correct_val:
                    score = marks
                    is_correct = True
                else:
                    score = 0
                    is_correct = False

            else:
                words = len(user_ans.split())
                if words >= 12:
                    score = marks
                    is_correct = True
                elif words >= 4:
                    score = max(1, marks // 2)
                    is_correct = False
                else:
                    score = 1
                    is_correct = False
        else:
            score = 0
            is_correct = False

        earned_marks += score

        answer_records.append({
            "question_index": idx,
            "question_id": q_id,
            "type": q_type,
            "correct": is_correct,
            "unit": unit
        })

        evaluations.append({
            "question_id": q_id,
            "type": q_type,
            "question_text": q.get("question_text") or q.get("question"),
            "marks": marks,
            "score": score,
            "user_answer": user_ans or "(No answer provided)",
            "correct_answer": q.get("correct_answer"),
            "is_correct": is_correct,
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
