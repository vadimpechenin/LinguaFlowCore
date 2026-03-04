from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class WordCreate(BaseModel):
    texten: str
    transcription: Optional[str]
    textl: Optional[str]
    partofspeech: Optional[str]
    examplesentence: Optional[str]
    difficultylevel: str
    #audiourl: Optional[str]
    #createdat: datetime


class WordRead(WordCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)

class WordResponse(BaseModel):
    id: str
    texten: str
    transcription: str | None
    textl: str
    partofspeech: str | None
    examplesentence: str | None
    difficultylevel: str
    audiourl: str | None
    createdat: datetime

class WordRecomendationResponse(BaseModel):
    id: str
    texten: str
    difficultylevel: str