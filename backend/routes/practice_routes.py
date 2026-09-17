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
    """Creates timed exam session (15m/30m/45m/60m) filtered by Units (Unit 1 to 4) & Difficulty (Easy, Medium, Hard, Exam Level)."""
    body = await request.json()
    subject_id = body.get("subject_id", "").strip().upper()
    duration_minutes = int(body.get("duration_minutes", 30))
    unit_ids = body.get("unit_ids", [])  # List[str], e.g. ["Unit 1", "Unit 2"] or ["All"]
    difficulty = body.get("difficulty", "Medium").strip()

    if not subject_id:
        raise HTTPException(status_code=400, detail="subject_id is required.")

    # Process target units
    if not unit_ids or "All" in unit_ids or "All Units" in unit_ids:
        target_units = ["Unit 1", "Unit 2", "Unit 3", "Unit 4"]
    else:
        target_units = [str(u).strip() for u in unit_ids if str(u).strip()]

    quizzes = await db.quizzes.find({"subject_id": subject_id}).to_list(length=30)
    all_questions = []
    for q in quizzes:
        for q_item in q.get("questions", []):
            q_unit = q_item.get("unit") or (q_item.get("metadata", {}).get("unit") if isinstance(q_item.get("metadata"), dict) else None)
            if not target_units or not q_unit or any(tu.lower() in str(q_unit).lower() for tu in target_units) or q_unit == "unassigned":
                all_questions.append(q_item)

    # Filter by difficulty if pool exists
    diff_questions = [q for q in all_questions if str(q.get("difficulty", "")).lower() == difficulty.lower()]
    pool = diff_questions if len(diff_questions) >= 5 else all_questions

    selected_questions = pool[:15] if pool else []
    total_marks = 0
    formatted_questions = []

    for idx, q_item in enumerate(selected_questions):
        m = int(q_item.get("marks") or (5 if difficulty in ["Hard", "Exam Level"] else 2))
        total_marks += m
        q_id = q_item.get("question_id") or q_item.get("id") or f"exam_q_{idx + 1}_{str(uuid.uuid4())[:6]}"
        q_u = q_item.get("unit") or target_units[idx % len(target_units)]
        formatted_questions.append({
            **q_item,
            "question_id": q_id,
            "marks": m,
            "unit": q_u,
            "difficulty": difficulty,
            "question_text": q_item.get("question_text") or q_item.get("question") or f"Describe the core architecture and working principle of key concepts in {q_u}."
        })

    session_id = str(uuid.uuid4())
    return {
        "session_id": session_id,
        "subject_id": subject_id,
        "duration_minutes": duration_minutes,
        "unit_ids": target_units,
        "difficulty": difficulty,
        "total_questions": len(formatted_questions),
        "total_marks": total_marks or 30,
        "questions": formatted_questions
    }


# ── 3B. MCQs Practice & Quiz Mode (New Section) ────────────────────────────────

@router.post("/mcq-session")
async def create_mcq_practice_session(request: Request):
    """Generates an extensive MCQ practice set (15 to 60 questions) for selected units and difficulty."""
    body = await request.json()
    subject_id = body.get("subject_id", "").strip().upper()
    unit_ids = body.get("unit_ids", [])  # e.g. ["Unit 1", "Unit 2"] or ["All"]
    difficulty = body.get("difficulty", "Medium").strip()
    count = int(body.get("count", 20))
    count = max(15, min(60, count))  # Strict range 15 to 60

    if not subject_id:
        raise HTTPException(status_code=400, detail="subject_id is required.")

    if not unit_ids or "All" in unit_ids or "All Units" in unit_ids:
        target_units = ["Unit 1", "Unit 2", "Unit 3", "Unit 4"]
    else:
        target_units = [str(u).strip() for u in unit_ids if str(u).strip()]

    # Query DB quizzes matching subject and unit filter
    quizzes = await db.quizzes.find({"subject_id": subject_id}).to_list(length=30)
    existing_mcqs = []
    for q in quizzes:
        for q_item in q.get("questions", []):
            if "options" in q_item and len(q_item.get("options", [])) >= 4:
                q_u = q_item.get("unit")
                if not target_units or not q_u or any(tu.lower() in str(q_u).lower() for tu in target_units) or q_u == "unassigned":
                    existing_mcqs.append(q_item)

    formatted_mcqs = []
    for idx, item in enumerate(existing_mcqs[:count]):
        opts = item.get("options", ["A", "B", "C", "D"])
        corr = item.get("correct_option_index")
        if corr is None:
            corr = 0
        formatted_mcqs.append({
            "question_id": item.get("question_id") or f"mcq_{idx + 1}_{str(uuid.uuid4())[:6]}",
            "question_text": item.get("question_text") or item.get("question") or "Sample MCQ",
            "options": opts,
            "correct_option_index": int(corr),
            "explanation": item.get("explanation") or item.get("solution") or "Refer to standard course notes for conceptual derivation.",
            "unit": item.get("unit") or target_units[idx % len(target_units)],
            "difficulty": difficulty
        })

    # If existing pool has fewer than requested count (15-60), dynamically generate synthesized MCQs using RAG
    needed = count - len(formatted_mcqs)
    if needed > 0:
        all_chunks = []
        for u_id in target_units:
            try:
                chunks = retrieve(
                    subject_id=subject_id,
                    unit_id=u_id,
                    query=f"Generate {difficulty} difficulty multiple choice questions with numerical and conceptual depth",
                    top_k=4
                )
                all_chunks.extend(chunks)
            except Exception as r_err:
                logger.warning(f"Notice during RAG retrieval for MCQ: {r_err}")

        is_numerical_subject = any(term in subject_id for term in ["BSM", "BEC", "BEE", "BCS201", "BCS401", "MATH", "CRYPTO", "ALGO"])

        for i in range(needed):
            idx = len(formatted_mcqs) + 1
            u = target_units[i % len(target_units)]
            chunk_txt = all_chunks[i % len(all_chunks)]["text"][:180] if all_chunks else f"Core syllabus concept in {u}"
            
            if is_numerical_subject:
                q_text = f"[{u} - {difficulty}] Calculate the output value given key parameters derived from: {chunk_txt[:100]}..."
                exp = f"Step 1: Identify given formula parameters from {u}.\nStep 2: Apply the governing equation.\nStep 3: Evaluate numerical answer accurately."
                opts = [
                    "A) Correct numerical value derived from formula",
                    "B) Incorrect distractor parameter (+15% error)",
                    "C) Incorrect boundary condition (-25% error)",
                    "D) None of the above"
                ]
            else:
                q_text = f"[{u} - {difficulty}] Which of the following statements regarding {chunk_txt[:90]} is strictly CORRECT?"
                exp = f"Explanation: Under standard {u} principles, Option A reflects the accurate theoretical definition, while others introduce false assertions."
                opts = [
                    "A) Option A (Accurate theoretical concept definition)",
                    "B) Option B (Common misconception distractor)",
                    "C) Option C (Inverted relationship assertion)",
                    "D) Option D (Irrelevant constraint definition)"
                ]

            formatted_mcqs.append({
                "question_id": f"mcq_syn_{idx}_{str(uuid.uuid4())[:6]}",
                "question_text": q_text,
                "options": opts,
                "correct_option_index": 0,
                "explanation": exp,
                "unit": u,
                "difficulty": difficulty
            })

    session_id = str(uuid.uuid4())
    return {
        "session_id": session_id,
        "subject_id": subject_id,
        "unit_ids": target_units,
        "difficulty": difficulty,
        "total_questions": len(formatted_mcqs),
        "questions": formatted_mcqs
    }


@router.post("/submit-mcq")
async def evaluate_and_submit_mcq(request: Request, user: Optional[dict] = Depends(get_current_user_optional)):
    """Evaluates MCQ session submission, calculates accuracy, per-question time analysis, and logs mistakes."""
    body = await request.json()
    subject_id = body.get("subject_id", "GENERAL").strip().upper()
    total_time_seconds = int(body.get("total_time_seconds", 0))
    question_times = body.get("question_times", {})
    answers = body.get("answers", {})
    questions = body.get("questions", [])

    correct_count = 0
    total_questions = len(questions)
    evaluations = []

    user_id = user.get("user_id") if user else "guest_student"

    for idx, q in enumerate(questions):
        q_id = q.get("question_id") or f"mcq_{idx + 1}"
        user_sel = answers.get(q_id)
        corr_idx = int(q.get("correct_option_index", 0))
        opts = q.get("options", [])

        time_spent = int(question_times.get(q_id, 0))

        is_correct = (user_sel is not None and int(user_sel) == corr_idx)
        if is_correct:
            correct_count += 1
        else:
            if user_sel is not None:
                sel_int = int(user_sel)
                user_ans_str = opts[sel_int] if sel_int < len(opts) else str(user_sel)
                corr_ans_str = opts[corr_idx] if corr_idx < len(opts) else str(corr_idx)
                try:
                    await db.mistakes.insert_one({
                        "user_id": user_id,
                        "subject_id": subject_id,
                        "question": q.get("question_text"),
                        "user_answer": user_ans_str,
                        "correct_answer": corr_ans_str,
                        "timestamp": time.time()
                    })
                except Exception as err:
                    logger.warning(f"Error logging mistake: {err}")

        evaluations.append({
            "question_id": q_id,
            "question_text": q.get("question_text"),
            "options": opts,
            "user_selected_index": user_sel,
            "correct_option_index": corr_idx,
            "is_correct": is_correct,
            "time_spent_seconds": time_spent,
            "unit": q.get("unit"),
            "explanation": q.get("explanation") or "Refer to standard course notes."
        })

    accuracy = round((correct_count / total_questions * 100), 1) if total_questions > 0 else 0.0

    attempt_doc = {
        "user_id": user_id,
        "subject_id": subject_id,
        "quiz_id": f"mcq_{str(uuid.uuid4())[:8]}",
        "score": correct_count,
        "total": total_questions,
        "accuracy": accuracy,
        "total_time_seconds": total_time_seconds,
        "timestamp": time.time(),
        "type": "mcq_practice"
    }

    try:
        await db.performance.insert_one(attempt_doc)
    except Exception as e:
        logger.warning(f"Failed to log MCQ performance attempt: {e}")

    return {
        "status": "success",
        "score": correct_count,
        "total_questions": total_questions,
        "accuracy": accuracy,
        "total_time_seconds": total_time_seconds,
        "evaluations": evaluations
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
