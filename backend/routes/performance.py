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
    clean_sub_id = subject_id.strip().upper()
    cursor = db.performance.find({"subject_id": clean_sub_id})
    attempts = await cursor.to_list(length=None)
    
    if not attempts:
        return {
            "total_quizzes": 0,
            "overall_accuracy": 0.0,
            "grade": "N/A",
            "total_time_minutes": 0.0,
            "total_questions_answered": 0,
            "unit_mastery": [],
            "accuracy_trend": [],
            "weak_topics": [],
            "strong_topics": [],
            "recent_activity": []
        }
        
    total_quizzes = len(attempts)
    total_correct = 0
    total_questions = 0
    total_time_seconds = 0
    
    attempts.sort(key=lambda x: x.get("submitted_at", 0))
    
    trend = []
    recent_activity = []
    unit_stats = defaultdict(lambda: {"correct": 0, "total": 0})
    
    for i, attempt in enumerate(attempts):
        score = attempt.get("score", 0)
        total = attempt.get("total", 0)
        total_correct += score
        total_questions += total
        t_sec = attempt.get("time_taken_seconds", 0)
        total_time_seconds += t_sec
        
        acc = round((score / total * 100), 1) if total > 0 else 0.0
        att_type = attempt.get("type", "quiz")
        
        trend.append({
            "attempt_num": i + 1,
            "score": score,
            "total": total,
            "accuracy": acc,
            "type": att_type
        })

        recent_activity.append({
            "quiz_id": attempt.get("quiz_id"),
            "attempt_num": i + 1,
            "score": score,
            "total": total,
            "accuracy": acc,
            "time_formatted": f"{t_sec // 60}m {t_sec % 60}s" if t_sec > 0 else "N/A",
            "type": "Timed Exam" if att_type == "timed_exam" else "Practice Quiz",
            "submitted_at": attempt.get("submitted_at")
        })
        
        for ans in attempt.get("answers", []):
            if isinstance(ans, dict):
                u = ans.get("unit") or "Unit 1"
                unit_stats[u]["total"] += 1
                if ans.get("correct"):
                    unit_stats[u]["correct"] += 1
                
    overall_accuracy = round((total_correct / total_questions * 100), 1) if total_questions > 0 else 0.0
    
    unit_mastery = []
    weak_topics = []
    strong_topics = []

    for u, stats in unit_stats.items():
        u_acc = round((stats["correct"] / stats["total"] * 100), 1) if stats["total"] > 0 else 0.0
        status = "Mastered" if u_acc >= 75 else "Proficient" if u_acc >= 50 else "Needs Review"
        unit_mastery.append({
            "unit_id": u,
            "accuracy": u_acc,
            "total_questions": stats["total"],
            "status": status
        })
        if u_acc < 60:
            weak_topics.append(u)
        else:
            strong_topics.append(u)

    if overall_accuracy >= 85:
        grade = "A+"
    elif overall_accuracy >= 75:
        grade = "A"
    elif overall_accuracy >= 60:
        grade = "B"
    elif overall_accuracy >= 45:
        grade = "C"
    else:
        grade = "D"
        
    return {
        "total_quizzes": total_quizzes,
        "overall_accuracy": overall_accuracy,
        "grade": grade,
        "total_time_minutes": round(total_time_seconds / 60, 1),
        "total_questions_answered": total_questions,
        "unit_mastery": unit_mastery,
        "accuracy_trend": trend,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "recent_activity": list(reversed(recent_activity))[:10]
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
