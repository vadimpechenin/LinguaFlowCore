from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from datetime import datetime, timedelta
from app.api.deps import get_db
from app.core.settings import ML_SERVICE_URL
from app.crud.progress import review_word, seed_user_progress
from app.api.deps import get_current_user
from app.crud.setting import get_settings
from app.db.models.progress import UserWordProgress
from app.db.models.review import WordReview
from app.db.models.word import Word
from app.schemas.progress import (
    ReviewResult,
    ProgressSummary,
    ProgressWordResponse,
    ProgressWord, ProgressWords, UserProgressFeaturesWord, RecommendWord, ProgressWordAnswer, AnswerProgress
)
from app.services.ml_client import MLClient, get_ml_client
from app.services.pipelines.progress_service import ProgressService
from app.services.pipelines.review_service import ReviewService
from app.services.pipelines.review_updater import ReviewUpdater

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/progress", response_model=UserProgressFeaturesWord)
def review(
    data: ProgressWords,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    ml: MLClient = Depends(get_ml_client),
):
    #ml_result = ml.get_next_review(history)
    result = None
    return result

@router.post("/progress/seed", response_model=UserProgressFeaturesWord)
def review(
    data: ProgressWords,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    ml: MLClient = Depends(get_ml_client),
):
    #ml_result = ml.get_next_review(history)
    result = seed_user_progress(
        db,
        user.id,
        data.word_ids,
        data.is_known
    )
    return result

#1 Получить слова для повторения
@router.get("/words", response_model=list[RecommendWord])
async def get_review_words(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    service = ReviewService()
    words = service.get_words_for_review(
        db,
        user.id
    )
    #TODO код, который пока использовать не будем
    """
    user_settings = get_settings(
        db,
        user.id
    )
    #Обращение к серверу ml для рекомендаций слов
    result = await ml_client.recommend(
        words, user_settings.dailywordlimit
    )

    if result is None:
        raise HTTPException(
            status_code=503,
            detail="ML Service unavailable"
        )
    """

    return words


#2 Отправка результата ответа
@router.post("/answer", response_model=ProgressWordAnswer)
async def answer(
    data: AnswerProgress,
   db: Session = Depends(get_db),
   user=Depends(get_current_user)
):

   updater = ReviewUpdater()

   return updater.process_answer(
       db,
       user.id,
       data.wordid,
       data.iscorrect,
       data.response_time_ms
   )


#4 Общий прогресс
@router.get("/progress/summary", response_model=ProgressSummary)
def progress_summary(user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = ProgressService()
    return service.get_summary(db, user.id)

"""
return ProgressSummary(
        total_words=total_words,
        learned_words=learned,
        daily_streak=0,  # можно добавить позже
        success_rate=round(success_rate, 2),
    )
"""
#3 Прогресс по слову
@router.get("/progress/word/{word_id}", response_model=ProgressWordResponse)
def word_progress(
    word_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ProgressService()
    return service.get_word_progress(db, user.id, word_id)

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





