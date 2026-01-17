from pydantic import BaseModel, ConfigDict
from typing import Optional


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