from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import List

#TODO еще может меняться
class ExamStart(BaseModel):
    difficultylevel: str
    size: int

class ExamQuestion(BaseModel):
    wordid: str
    question: str

class ExamResponse(BaseModel):
    examid: str
    questions: List[dict]
    #questions: List[ExamQuestion]

class ExamResponseAllFields(BaseModel):
    id : str
    userid : str
    difficultylevel: str
    size: int
    takenat: datetime

    #model_config = ConfigDict(from_attributes=True)

class ExamSubmit(BaseModel):
    answers: list

class ExamResult(BaseModel):
    score: int
    estimatedlevel: str
