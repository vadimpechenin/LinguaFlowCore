from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.progress import ReviewResult
from crud.progress import review_word

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/{user_id}/{word_id}")
def review(
    user_id: str,
    word_id: str,
    data: ReviewResult,
    db: Session = Depends(get_db),
):
    review_word(
        db,
        user_id,
        word_id,
        data.is_correct,
        data.response_time_ms,
    )
    return {"status": "ok"}