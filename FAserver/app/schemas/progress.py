from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

class ProgressWords(BaseModel):
    word_ids: list[str]
    is_known: bool

class ProgressWordResponse(BaseModel):
    reviewcount: int| None
    successrate: float| None
    nextreviewat: datetime | None

class UserProgressFeaturesWord(BaseModel):
    progress_created: int
    features_created: int

class ProgressSummary(BaseModel):
    total_words: int | None
    learned_words: int | None
    daily_streak: int | None
    success_rate: float| None

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

class ReviewWordsResponse(BaseModel):
    words: List[RecommendWord]
    was_refreshed: bool  # Флаг: был ли создан новый набор

class RefreshWords(BaseModel):
    refresh:bool

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