from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import UserWordProgress, WordReview


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