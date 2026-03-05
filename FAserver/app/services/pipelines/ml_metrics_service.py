from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.models import UserWordProgress, MLWordFeatures


class MLMetricsService:

    def update_word_metrics(
        self,
        db: Session,
        word_id: str
    ):

        # -----------------------------
        # 1️Средний success rate
        # -----------------------------
        avg_success = (
            db.query(
                func.avg(UserWordProgress.successrate)
            )
            .filter(
                UserWordProgress.wordid == word_id
            )
            .scalar()
        ) or 0.0

        # -----------------------------
        # 2️Средний интервал
        # -----------------------------
        avg_interval = (
            db.query(
                func.avg(
                    func.extract(
                        "epoch",
                        UserWordProgress.nextreviewed
                        - UserWordProgress.lastreviewed
                    )
                )
            )
            .filter(
                UserWordProgress.wordid == word_id,
                UserWordProgress.lastreviewed.isnot(None),
                UserWordProgress.nextreviewed.isnot(None)
            )
            .scalar()
        )

        if avg_interval:
            avg_interval /= 86400  # секунды → дни
        else:
            avg_interval = 0.0

        # -----------------------------
        # 3️Frequency Rank
        # -----------------------------
        # Суммарное число повторений по каждому слову
        review_stats = (
            db.query(
                UserWordProgress.wordid,
                func.sum(UserWordProgress.reviewcount).label("total_reviews")
            )
            .group_by(UserWordProgress.wordid)
            .order_by(desc("total_reviews"))
            .all()
        )

        frequency_rank = None
        for index, row in enumerate(review_stats, start=1):
            if row.wordid == word_id:
                frequency_rank = index
                break

        if frequency_rank is None:
            frequency_rank = len(review_stats) + 1

        # -----------------------------
        # 4️⃣ Обновление / создание MLWordFeatures
        # -----------------------------
        features = (
            db.query(MLWordFeatures)
            .filter(MLWordFeatures.wordid == word_id)
            .first()
        )

        if not features:
            features = MLWordFeatures(wordid=word_id)
            db.add(features)

        features.avgsuccessrate = float(avg_success)
        features.avgreviewinterval = float(avg_interval)
        features.frequencyrank = frequency_rank


        db.commit()