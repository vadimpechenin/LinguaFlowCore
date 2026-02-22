from fastapi import APIRouter

from schemas.request import (
    RecommendationRequest,
    PredictRequest
)

from schemas.response import (
    RecommendationResponse,
    PredictResponse

)

from services.recommender import recommender
from services.predictor import predictor


router = APIRouter(
    prefix="/ml",
    tags=["ML"]
)


@router.post("/recommend",
    response_model=RecommendationResponse
)
def recommend(request: RecommendationRequest):
    result = recommender.recommend(
        request.words
    )


    return RecommendationResponse(
        recommendations=result
    )


@router.post("/predict",
    response_model=PredictResponse)
def predict(request: PredictRequest):
    probability, hours = predictor.predict(
        request.features
    )


    return PredictResponse(
        probability=probability,
        next_review_hours=hours
    )