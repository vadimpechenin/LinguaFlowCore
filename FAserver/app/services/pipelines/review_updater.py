from sqlalchemy.orm import Session

from app.db.models import UserWordProgress
from app.services.models.spaced_repetition_engine import SpacedRepetitionEngine


class ReviewUpdater:

   def __init__(self):
       self.spaced = SpacedRepetitionEngine()

   def process_answer(
       self,
       db: Session,
       user_id: str,
       word_id: str,
       is_correct: bool
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

       db.commit()

       return progress
