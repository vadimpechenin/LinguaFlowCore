from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from datetime import datetime, timedelta
from app.api.deps import get_db
from app.core.settings import ML_SERVICE_URL
from app.crud.progress import review_word, seed_user_progress
from app.api.deps import get_current_user
from app.crud.setting import get_settings
from app.schemas.progress import (
    ProgressSummary,
    ProgressWordResponse,
    ProgressWords, UserProgressFeaturesWord, ProgressWordAnswer, AnswerProgress, RefreshWords,
    ReviewWordsResponse
)
from app.services.ml_client import MLClient, get_ml_client
from app.services.pipelines.progress_service import ProgressService
from app.services.pipelines.review_service import ReviewService
from app.services.pipelines.review_updater import ReviewUpdater

router = APIRouter(prefix="/review", tags=["review"])


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
@router.post("/words", response_model=ReviewWordsResponse)
async def get_review_words(
    refreshWord: RefreshWords,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    print("Статус обновления слов: " + str(refreshWord.refresh))
    if (user!=None):
        print(user.id)
    service = ReviewService()
    user_settings = get_settings(
        db,
        user.id
    )
    words, was_refreshed = service.get_words_for_review(
        db,
        user.id,
        user_settings.dailywordlimit,
        refreshWord.refresh
    )
    return {
        "words": words,
        "was_refreshed": was_refreshed
    }
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
#5 Прогресс по слову
@router.get("/progress/word/{word_id}", response_model=ProgressWordResponse)
def word_progress(
    word_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = ProgressService()
    return service.get_word_progress(db, user.id, word_id)





