from sqlalchemy.orm import Session

from app.crud.progress import get_due_words, get_weak_words, get_new_words
from app.services.models.recommender_engine import RecommendationEngine


class ReviewService:


    def __init__(self):
        self.recommender = RecommendationEngine()


    def get_words_for_review(
        self,
        db: Session,
        user_id: str,
        limit: int = 20
    ):

        words = []

        # 1️⃣ Просроченные
        due = get_due_words(
            db,
            user_id,
            limit
        )

        words.extend(
            [p.word for p in due]
        )

        if len(words) >= limit:
            return words[:limit]

        # 2️⃣ Слабые
        weak = get_weak_words(
            db,
            user_id,
            limit - len(words)
        )

        words.extend(
            [p.word for p in weak]
        )

        if len(words) >= limit:
            return words[:limit]

        # 3️⃣ Новые
        new_words = get_new_words(
            db,
            user_id,
            limit - len(words)
        )
        words.extend(new_words)

        return words[:limit]
