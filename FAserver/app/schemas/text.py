from pydantic import BaseModel


class TextRequest(BaseModel):
    title: str
    content: str
    language: str

class TextResponse(BaseModel):
    id: str
    title: str
    content: str


class TextAnalyzeResponse(BaseModel):
    title: str
    level: str
    unknown_words: int
    coveragepercent: float
    recommended_words: list[str]


