from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import UserWordProgress, WordReview
from app.services.models.spaced_repetition_engine import SpacedRepetitionEngine
from app.services.pipelines.ml_metrics_service import MLMetricsService


class ReviewUpdater:

   def __init__(self):
       self.spaced = SpacedRepetitionEngine()
       self.ml_metrics = MLMetricsService()

   def process_answer(
       self,
       db: Session,
       user_id: str,
       word_id: str,
       is_correct: bool,
       response_time_ms: int
   ):

       progress = (
           db.query(UserWordProgress)
           .filter(
               UserWordProgress.userid == user_id,
               UserWordProgress.wordid == word_id
           )
           .first()
       )

       progress = self.spaced.update(
           progress,
           is_correct
       )

       review = WordReview(
           id=UUIDClass.geterateUUIDWithout_(),
           userid=user_id,
           wordid=word_id,
           iscorrect=is_correct,
           responsetimems=response_time_ms
       )

       db.add(review)

       db.commit()

       self.ml_metrics.update_word_metrics(
           db,
           word_id
       )

       return progress
