from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import UserWordProgress, WordReview


class ProgressService:

   # ---------------------------------------
   # 6.1 Общий прогресс пользователя
   # ---------------------------------------
   def get_summary(self, db: Session, user_id: str):

       total_words = (
           db.query(UserWordProgress)
           .filter(UserWordProgress.userid == user_id)
           .count()
       )

       learned_words = (
           db.query(UserWordProgress)
           .filter(
               UserWordProgress.userid == user_id,
               UserWordProgress.isknown == True
           )
           .count()
       )

       avg_success = (
           db.query(func.avg(UserWordProgress.successrate))
           .filter(UserWordProgress.userid == user_id)
           .scalar()
       ) or 0.0

       streak = self._calculate_daily_streak(db, user_id)

       return {
           "total_words": total_words,
           "learned_words": learned_words,
           "daily_streak": streak,
           "success_rate": round(float(avg_success), 2)
       }

   # ---------------------------------------
   # 6.2 Прогресс по слову
   # ---------------------------------------
   def get_word_progress(self, db: Session, user_id: str, word_id: str):

       progress = (
           db.query(UserWordProgress)
           .filter(
               UserWordProgress.userid == user_id,
               UserWordProgress.wordid == word_id
           )
           .first()
       )

       if not progress:
           return {
           "reviewcount": None,
           "successrate": None,
           "nextreviewat": None
       }

       return {
           "reviewcount": progress.reviewcount,
           "successrate": round(progress.successrate, 2),
           "nextreviewat": progress.nextreviewed
       }

   # ---------------------------------------
   # Расчет дневного прогресса
   # ---------------------------------------
   def _calculate_daily_streak(self, db: Session, user_id: str):

       today = datetime.utcnow().date()

       review_dates = (
           db.query(func.date(WordReview.reviewedat))
           .filter(WordReview.userid == user_id)
           .distinct()
           .order_by(func.date(WordReview.reviewedat).desc())
           .all()
       )

       review_dates = [r[0] for r in review_dates]

       streak = 0
       current_day = today

       for date in review_dates:
           if date == current_day:
               streak += 1
               current_day -= timedelta(days=1)
           elif date < current_day:
               break

       return streak
