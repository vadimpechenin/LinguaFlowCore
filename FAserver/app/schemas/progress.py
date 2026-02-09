from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewResult(BaseModel):
    is_correct: bool
    response_time_ms: Optional[int]

class ProgressWord(BaseModel):
    client_id: str
    word_id: str
    is_correct: bool
    response_time_ms: Optional[int]

class ProgressWordResponse(BaseModel):
    reviewcount: int
    successrate: float
    nextreviewed: datetime | None

class ProgressSummary(BaseModel):
    total_words: int
    learned_words: int
    daily_streak: int
    success_rate: float