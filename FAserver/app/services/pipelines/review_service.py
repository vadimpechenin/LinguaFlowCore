from sqlalchemy.orm import Session

from app.crud.progress import get_due_words, get_weak_words, get_new_words
from app.db.models import UserWordProgress
from app.services.pipelines.forgetting_curve import ForgettingCurveEngine


class ReviewService:


    def __init__(self):
        self.forgetting = ForgettingCurveEngine()

    def get_words_for_review(
        self,
        db: Session,
        user_id: str,
        limit: int = 20
    ):

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

        return [
            word for word, _ in ranked[:limit]
        ]
