"""
Логика рекомендаций
"""


class Recommender:

    def recommend(
        self,
        words
    ):
        # пример логики
        sorted_words = sorted(
            words,
            key=lambda x: x["difficulty"]
        )

        result = [
            w["id"]
            for w in sorted_words[:10]
        ]
        return result


recommender = Recommender()