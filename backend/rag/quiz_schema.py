from pydantic import BaseModel, Field
from typing import List

class QuizQuestion(BaseModel):
    question_text: str = Field(..., description="The text of the multiple choice question.")
    options: List[str] = Field(..., min_length=4, max_length=4, description="Exactly 4 options.")
    correct_option_index: int = Field(..., ge=0, le=3, description="Index of the correct option (0-3).")
    explanation: str = Field(..., description="Detailed explanation of the answer.")
    source_chunk_ids: List[str] = Field(..., description="IDs of chunks used to ground this question.")
    unit: str = Field(..., description="The unit this question belongs to.")
    difficulty: str = Field(..., description="Basic, Intermediate, or Advanced.")

class QuizResponse(BaseModel):
    questions: List[QuizQuestion]
