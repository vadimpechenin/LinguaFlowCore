from datetime import datetime

from pydantic import BaseModel
from typing import List

#TODO еще может меняться
class ExamStart(BaseModel):
    difficultylevel: str
    size: int

class ExamResponse(BaseModel):
    examid: str
    questions: List[dict]

class ExamResponseAllFields(BaseModel):
    id : str
    userid : str
    difficultylevel: str
    size: int
    takenat: datetime

class ExamSubmit(BaseModel):
    answers: list

class ExamResult(BaseModel):
    score: int
    estimatedlevel: str
