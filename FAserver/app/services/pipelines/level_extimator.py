class LevelEstimator:

   def estimate(self, difficulty: str, score_percent: float):

       if score_percent > 85:
           return self._upgrade(difficulty)
       elif score_percent < 50:
           return self._downgrade(difficulty)
       return difficulty

   def _upgrade(self, level):
       order = ["A1", "A2", "B1", "B2", "C1", "C2"]
       idx = order.index(level)
       return order[min(idx + 1, len(order) - 1)]

   def _downgrade(self, level):
       order = ["A1", "A2", "B1", "B2", "C1", "C2"]
       idx = order.index(level)
       return order[max(idx - 1, 0)]
