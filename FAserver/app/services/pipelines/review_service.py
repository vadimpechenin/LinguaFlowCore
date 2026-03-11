from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.progress import get_due_words, get_weak_words, get_new_words
from app.db.models import UserWordProgress, Word
from app.db.models.review_session import ReviewSession
from app.db.models.review_session_words import ReviewSessionWord
from app.services.pipelines.forgetting_curve import ForgettingCurveEngine
from datetime import datetime, date
from app.db.core.support.UUIDClass import UUIDClass


class ReviewService:


    def __init__(self):
        self.forgetting = ForgettingCurveEngine()

    def get_words_for_review(
        self,
        db: Session,
        user_id: str,
        limit: int = 10,
        refresh: bool=False
    ):
        today = date.today()

        session = (
            db.query(ReviewSession)
            .filter(
                ReviewSession.userid == user_id,
                func.date(ReviewSession.createdat) == today
            )
            .first()
        )

        # если есть сессия и refresh = False → вернуть те же слова
        if session and not refresh:
            words = (
                db.query(Word)
                .join(
                    ReviewSessionWord,
                    ReviewSessionWord.wordid == Word.id
                )
                .filter(
                    ReviewSessionWord.sessionid == session.id
                )
                .all()
            )

            return words

        # иначе создаём новую выборку

        progresses = (
            db.query(UserWordProgress)
            .filter(
                UserWordProgress.userid == user_id
            )
            .all()
        )

        ranked = []

        for progress in progresses:
            score = self.forgetting.priority_score(
                progress.lastreviewed,
                progress.reviewcount,
                progress.successrate
            )

            ranked.append(
                (progress.word, score)
            )

        ranked.sort(
            key=lambda x: x[1],
            reverse=True
        )
        words = [
            word for word, _ in ranked[:limit]
        ]
        # создаём новую сессию
        session = ReviewSession(
            id=UUIDClass.geterateUUIDWithout_(),
            userid=user_id,
            createdat=datetime.utcnow()
        )

        db.add(session)
        db.flush()

        for word in words:
            db.add(
                ReviewSessionWord(
                    id=UUIDClass.geterateUUIDWithout_(),
                    sessionid=session.id,
                    wordid=word.id
                )
            )

        db.commit()

        return words
