from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewResult(BaseModel):
    is_correct: bool
    response_time_ms: Optional[int]