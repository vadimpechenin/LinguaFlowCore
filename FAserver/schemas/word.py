from pydantic import BaseModel
from typing import Optional


class WordCreate(BaseModel):
    text_en: str
    transcription: Optional[str]
    text_ru: Optional[str]
    example_sentence: Optional[str]
    difficulty_level: str


class WordRead(WordCreate):
    id: str

    class Config:
        orm_mode = True