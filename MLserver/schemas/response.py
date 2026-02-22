from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    recommendations: list[str]


class PredictResponse(BaseModel):
    probability: float
    next_review_hours: int