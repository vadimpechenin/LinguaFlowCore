from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from datetime import datetime, timedelta
from app.api.deps import get_db, get_ml_client
from app.core.settings import ML_SERVICE_URL
from app.crud.progress import review_word
from app.api.deps import get_current_user
from app.db.models.progress import UserWordProgress
from app.db.models.review import WordReview
from app.db.models.word import Word
from app.schemas.progress import (
    ReviewResult,
    ProgressSummary,
    ProgressWordResponse,
    ProgressWord
)
from app.services.ml_client import MLClient

router = APIRouter(prefix="/review", tags=["review"])



@router.post("/{user_id}/{word_id}")
def review(
    user_id: str,
    word_id: str,
    data: ReviewResult,
    db: Session = Depends(get_db),
):
    review_word(
        user_id,
        word_id,
        data,
        db
    )
    return {"status": "ok"}


@router.post("/progress")
def review(
    data: ProgressWord,
    db: Session = Depends(get_db),
    ml: MLClient = Depends(get_ml_client),
):
    ml_result = ml.get_next_review(history)
    review_word(
        db,
        data.user_id,
        data.word_id,
        json={"is_correct": data.is_correct,
              "response_time_ms": data.response_time_ms},
    )
    return {"status": "ok"}

#1 Получить слова для повторения
@router.get("/next")
async def get_next_review(user=Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(UserWordProgress).filter_by(user_id=user.id).all()

    payload = {
        "user_id": user.id,
        "history": [
            {
                "word_id": h.word_id,
                "success_rate": h.success_rate,
                "last_review": h.updated_at.isoformat() if h.updated_at else None,
            }
            for h in history
        ],
    }

    async with httpx.AsyncClient(timeout=3) as client:
        resp = await client.post(f"{ML_SERVICE_URL}/ml/review/next", json=payload)
        resp.raise_for_status()

    word_ids = [w["word_id"] for w in resp.json()["recommended_words"]]
    return db.query(Word).filter(Word.id.in_(word_ids)).all()

#2 Отправка результата ответа
@router.post("/review/{user_id}/{word_id}")
async def review_word(
    user_id: str,
    word_id: str,
    data: ReviewResult,
    db: Session = Depends(get_db),
):
    progress = (
        db.query(UserWordProgress)
        .filter_by(user_id=user_id, word_id=word_id)
        .first()
    )

    if not progress:
        progress = UserWordProgress(
            user_id=user_id,
            word_id=word_id,
            review_count=0,
            success_rate=0.0,
        )
        db.add(progress)

    # сохранить review
    review = WordReview(
        user_id=user_id,
        word_id=word_id,
        is_correct=data.is_correct,
        response_time_ms=data.response_time_ms,
    )
    db.add(review)

    # ML update
    async with httpx.AsyncClient(timeout=3) as client:
        ml_resp = await client.post(
            f"{ML_SERVICE_URL}/ml/review/update",
            json={
                "word_id": word_id,
                "is_correct": data.is_correct,
                "response_time_ms": data.response_time_ms,
                "review_count": progress.review_count,
            },
        )
        ml_resp.raise_for_status()
        ml_data = ml_resp.json()

    progress.review_count += 1
    progress.success_rate = (
        (progress.success_rate * (progress.review_count - 1))
        + (1 if data.is_correct else 0)
    ) / progress.review_count

    progress.next_review_at = datetime.utcnow() + timedelta(
        hours=ml_data["next_review_in_hours"]
    )

    db.commit()
    return {"status": "ok"}

#3 Прогресс по слову
@router.get("/progress/word/{word_id}", response_model=ProgressWordResponse)
def word_progress(
    word_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress = (
        db.query(UserWordProgress)
        .filter_by(user_id=user.id, word_id=word_id)
        .first()
    )
    if not progress:
        raise HTTPException(404, "No progress")
    return progress

#4 Общий прогресс
@router.get("/progress/summary", response_model=ProgressSummary)
def progress_summary(user=Depends(get_current_user), db: Session = Depends(get_db)):
    total_words = db.query(Word).count()
    learned = (
        db.query(UserWordProgress)
        .filter(
            UserWordProgress.user_id == user.id,
            UserWordProgress.success_rate > 0.8,
        )
        .count()
    )

    avg_success = (
        db.query(UserWordProgress)
        .filter_by(user_id=user.id)
        .with_entities(UserWordProgress.success_rate)
        .all()
    )

    success_rate = (
        sum(r[0] for r in avg_success) / len(avg_success)
        if avg_success
        else 0.0
    )

    return ProgressSummary(
        total_words=total_words,
        learned_words=learned,
        daily_streak=0,  # можно добавить позже
        success_rate=round(success_rate, 2),
    )