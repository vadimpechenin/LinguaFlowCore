from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    user_id: str
    words: list[dict]


class PredictRequest(BaseModel):
    user_id: str
    word_id: str
    features: dict