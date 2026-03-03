from datetime import datetime
import math

DAY_TO_SECOND = 86400


class ForgettingCurveEngine:

   def __init__(self, base_decay: float = 0.35):
       self.base_decay = base_decay

   def recall_probability(
       self,
       last_reviewed,
       review_count: int,
       success_rate: float
   ) -> float:

       if not last_reviewed:
           return 0.0

       now = datetime.utcnow()
       delta_days = (
           now - last_reviewed.replace(tzinfo=None)
       ).total_seconds() / DAY_TO_SECOND

       decay = (
           self.base_decay
           / (1 + review_count)
       ) * (1 - success_rate + 0.1)

       probability = math.exp(
           -decay * delta_days
       )

       return probability

   def priority_score(
       self,
       last_reviewed,
       review_count,
       success_rate
   ):

       p = self.recall_probability(
           last_reviewed,
           review_count,
           success_rate
       )

       return 1 - p
