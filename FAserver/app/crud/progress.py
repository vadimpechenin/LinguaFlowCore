from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import UserWordProgress, WordReview, MLWordFeatures, Word
from sqlalchemy import func


def review_word(
    db: Session,
    user_id: str,
    word_id: str,
    is_correct: bool,
    response_time_ms: int | None,
):
    progress = (
        db.query(UserWordProgress)
        .filter_by(userid=user_id, wordid=word_id)
        .first()
    )

    if not progress:
        ID = UUIDClass.geterateUUIDWithout_()
        progress = UserWordProgress(
            id=ID,
            userid=user_id,
            wordid=word_id,
            reviewcount = 0,
            successrate = 0,
        )
        db.add(progress)

    progress.reviewcount += 1
    progress.lastreviewed = datetime.utcnow()

    if is_correct:
        progress.successrate = min(progress.successrate + 0.1, 1.0)
        progress.nextrevied = datetime.utcnow() + timedelta(days=3)
    else:
        progress.successrate = max(progress.successrate - 0.2, 0.0)
        progress.nextrevied = datetime.utcnow() + timedelta(days=1)

    ID = UUIDClass.geterateUUIDWithout_()

    review = WordReview(
        id = ID,
        userid=user_id,
        wordid=word_id,
        iscorrect=is_correct,
        responsetimems=response_time_ms,
    )

    db.add(review)
    db.commit()

def seed_user_progress(
    db: Session,
    user_id: str,
    word_ids: list[str],
    isknown: bool
):

    now = datetime.utcnow()

    created_progress = 0
    created_features = 0

    for word_id in word_ids:

        # ---------------------------
        # 1️⃣ UserWordProgress
        # ---------------------------

        exists = (
            db.query(UserWordProgress)
            .filter(
                UserWordProgress.userid == user_id,
                UserWordProgress.wordid == word_id
            )
            .first()
        )

        if not exists:

            progress = UserWordProgress(

                id=UUIDClass.geterateUUIDWithout_(),

                userid=user_id,
                wordid=word_id,

                lastreviewed=None,
                nextreviewed=now,

                successrate=0.0,
                reviewcount=0,
                isknown=isknown

            )

            db.add(progress)
            created_progress += 1

        # ---------------------------
        # 2️⃣ MLWordFeatures
        # ---------------------------

        features = (
            db.query(MLWordFeatures)
            .filter(
                MLWordFeatures.wordid == word_id
            )
            .first()
        )

        if not features:

            # средняя успешность по всем пользователям
            avg_success = (
                db.query(
                    func.avg(UserWordProgress.successrate)
                )
                .filter(
                    UserWordProgress.wordid == word_id
                )
                .scalar()
            )

            # средний интервал повторения
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
                    UserWordProgress.lastreviewed.isnot(None)
                )
                .scalar()
            )

            # если данных нет — дефолт
            if avg_success is None:
                avg_success = 0.0

            if avg_interval is None:
                avg_interval = 0.0
            else:
                avg_interval = avg_interval / 86400  # секунды → дни

            # frequency rank (заглушка или вычислить отдельно)
            frequency_rank = None

            features = MLWordFeatures(

                wordid=word_id,

                frequencyrank=frequency_rank,
                avgsuccessrate=avg_success,
                avgreviewinterval=avg_interval

            )

            db.add(features)
            created_features += 1

    db.commit()

    return {
        "progress_created": created_progress,
        "features_created": created_features
    }


#----------------------
#Блок методов для ReviewSelector
def get_due_words(
    db: Session,
    user_id: str,
    limit: int = 20
):

    now = datetime.utcnow()

    return (
        db.query(UserWordProgress)
        .join(Word)
        .filter(
            UserWordProgress.userid == user_id,
            UserWordProgress.nextreviewed <= now
        )
        .order_by(
            UserWordProgress.nextreviewed.asc()
        )
        .limit(limit)
        .all()
    )


def get_weak_words(
    db: Session,
    user_id: str,
    limit: int = 10
):

    return (
        db.query(UserWordProgress)
        .join(Word)
        .filter(
            UserWordProgress.userid == user_id,
            UserWordProgress.successrate < 0.6
        )
        .order_by(
            UserWordProgress.successrate.asc()
        )
        .limit(limit)
        .all()
    )


def get_new_words(
    db: Session,
    user_id: str,
    limit: int = 10
):

    subquery = (
        db.query(UserWordProgress.wordid)
        .filter(UserWordProgress.userid == user_id)
    )

    return (
        db.query(Word)
        .filter(~Word.id.in_(subquery))
        .limit(limit)
        .all()
    )