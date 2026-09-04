from fastapi import APIRouter, HTTPException
from models.performance import QuizAttempt, QuizSubmitRequest, AnswerRecord
from database import db
import time
from collections import defaultdict

performance_router = APIRouter()

@performance_router.post("/api/quiz/{quiz_id}/submit")
async def submit_quiz(quiz_id: str, req: QuizSubmitRequest):
    # Retrieve the stored quiz
    quiz = await db.quizzes.find_one({"quiz_id": quiz_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    user_id = quiz.get("user_id", "test_user")
    
    # Enforce Idempotency / No-Retakes
    existing_attempt = await db.performance.find_one({"quiz_id": quiz_id, "user_id": user_id})
    if existing_attempt:
        raise HTTPException(status_code=400, detail="Quiz already submitted")
        
    questions = quiz.get("questions", [])
    total = len(questions)
    
    score = 0
    answer_records = []
    
    for idx_str, selected_index in req.answers.items():
        try:
            idx = int(idx_str)
        except ValueError:
            continue
            
        if 0 <= idx < total:
            q = questions[idx]
            correct_option_index = q.get("correct_option_index")
            is_correct = (selected_index == correct_option_index)
            if is_correct:
                score += 1
                
            unit = q.get("unit", "unassigned")
            
            answer_records.append(AnswerRecord(
                question_index=idx,
                selected_index=selected_index,
                correct=is_correct,
                unit=unit
            ))
            
    attempt = QuizAttempt(
        user_id=quiz.get("user_id", "test_user"),
        subject_id=quiz.get("subject_id"),
        quiz_id=quiz_id,
        answers=answer_records,
        score=score,
        total=total,
        submitted_at=time.time()
    )
    
    await db.performance.insert_one(attempt.model_dump())
    
    return {"score": score, "total": total, "attempt_id": quiz_id}

@performance_router.get("/api/subjects/{subject_id}/performance")
async def get_subject_performance(subject_id: str):
    # Fetch all attempts for this subject
    cursor = db.performance.find({"subject_id": subject_id})
    attempts = await cursor.to_list()
    
    if not attempts:
        return {
            "total_quizzes": 0,
            "overall_accuracy": 0,
            "unit_mastery": [],
            "accuracy_trend": []
        }
        
    total_quizzes = len(attempts)
    total_correct = 0
    total_questions = 0
    
    # Sort attempts by submitted_at to get a sequential trend
    attempts.sort(key=lambda x: x.get("submitted_at", 0))
    
    trend = []
    unit_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    
    for i, attempt in enumerate(attempts):
        score = attempt.get("score", 0)
        total = attempt.get("total", 0)
        
        total_correct += score
        total_questions += total
        
        trend.append({
            "attempt_num": i + 1,
            "score": score,
            "total": total,
            "accuracy": (score / total * 100) if total > 0 else 0
        })
        
        for ans in attempt.get("answers", []):
            u = ans.get("unit", "unassigned")
            unit_stats[u]["total"] += 1
            if ans.get("correct"):
                unit_stats[u]["correct"] += 1
                
    overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    unit_mastery = []
    for u, stats in unit_stats.items():
        unit_mastery.append({
            "unit_id": u,
            "accuracy": (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0,
            "total_questions": stats["total"]
        })
        
    return {
        "total_quizzes": total_quizzes,
        "overall_accuracy": round(overall_accuracy, 1),
        "unit_mastery": unit_mastery,
        "accuracy_trend": trend
    }

@performance_router.get("/api/performance/overview")
async def get_performance_overview():
    cursor = db.performance.find()
    attempts = await cursor.to_list()
    
    subject_stats = defaultdict(lambda: {"correct": 0, "total": 0, "quizzes": 0})
    
    for attempt in attempts:
        sub = attempt.get("subject_id")
        if not sub:
            continue
        subject_stats[sub]["correct"] += attempt.get("score", 0)
        subject_stats[sub]["total"] += attempt.get("total", 0)
        subject_stats[sub]["quizzes"] += 1
        
    overview = []
    for sub, stats in subject_stats.items():
        overview.append({
            "subject_id": sub,
            "total_quizzes": stats["quizzes"],
            "accuracy": (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        })
        
    return {"subjects": overview}
