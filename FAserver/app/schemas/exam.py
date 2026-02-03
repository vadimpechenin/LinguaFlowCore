from pydantic import BaseModel
from typing import List

#TODO еще может меняться
class ExamStart(BaseModel):
    difficulty: str
    size: int = 20

class ExamQuestion(BaseModel):
    wordid: int
    question: str

class ExamResponse(BaseModel):
    examid: int
    questions: List[ExamQuestion]

class ExamSubmit(BaseModel):
    answers: list

class ExamResult(BaseModel):
    score: int
    estimated_level: str
