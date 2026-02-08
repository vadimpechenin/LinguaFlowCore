from pydantic import BaseModel
from typing import List

#TODO еще может меняться
class ExamStart(BaseModel):
    title: str
    difficultylevel: str
    score: float

class ExamQuestion(BaseModel):
    wordid: str
    question: str

class ExamResponse(BaseModel):
    examid: str
    questions: List[ExamQuestion]

class ExamSubmit(BaseModel):
    answers: list

class ExamResult(BaseModel):
    score: float
    estimated_level: str
