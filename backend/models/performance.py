from pydantic import BaseModel, Field
from typing import List, Dict

class AnswerRecord(BaseModel):
    question_index: int
    selected_index: int
    correct: bool
    unit: str

class QuizAttempt(BaseModel):
    user_id: str = "test_user"
    subject_id: str
    quiz_id: str
    answers: List[AnswerRecord]
    score: int
    total: int
    submitted_at: float

class QuizSubmitRequest(BaseModel):
    answers: Dict[str, int] = Field(..., description="Mapping of question index (as string) to selected option index")
