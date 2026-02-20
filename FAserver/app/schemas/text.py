from pydantic import BaseModel


class TextRequest(BaseModel):
    title: str
    content: str
    language: str

class TextResponse(BaseModel):
    id: str
    title: str
    content: str
"""
class TextAnalyzeResponse(BaseModel):
    totalwords = int
    knownwords = int
    unknownwords = int
    coveragepercent = float
    computedat: str | None
"""
