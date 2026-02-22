"""
Прогноз забываний
"""
import random


class Predictor:

    def predict(
        self,
        features
    ):
        probability = random.random()
        next_review = int(
            24 * (1 - probability)
        )

        return probability, next_review


predictor = Predictor()