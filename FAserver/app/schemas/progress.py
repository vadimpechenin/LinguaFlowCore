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

class ProgressWords(BaseModel):
    word_ids: list[str]
    is_known: bool

class ProgressWordResponse(BaseModel):
    reviewcount: int
    successrate: float
    nextreviewed: datetime | None

class UserProgressFeaturesWord(BaseModel):
    progress_created: int
    features_created: int

class ProgressSummary(BaseModel):
    total_words: int
    learned_words: int
    daily_streak: int
    success_rate: float

class RecommendWord(BaseModel):
    id: str
    texten: str
    transcription: str | None
    textl: str
    partofspeech: str
    examplesentence: str | None
    difficultylevel: str
    audiourl: str | None
    createdat: datetime

class ProgressWordAnswer(BaseModel):
    id: str
    userid: str
    wordid: str
    lastreviewed: datetime | None
    nextreviewed: datetime | None
    successrate: float
    reviewcount: int
    isknown: bool
    createdat: datetime

class AnswerProgress(BaseModel):
    wordid: str
    iscorrect: bool
    response_time_ms: int