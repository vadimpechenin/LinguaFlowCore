from typing import List, Dict
import httpx
import random

from app.core.settings import ML_SERVICE_URL


async def recommend(
    user_id,
    words
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ML_SERVICE_URL}/recommend",
            json={
                "user_id": user_id,
                "words": words
            }
        )

        return response.json()


async def predict(
    user_id,
    word_id,
    features
):


    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ML_SERVICE_URL}/predict",
            json={
                "user_id": user_id,
                "word_id": word_id,
                "features": features
            }
        )

        return response.json()


class MLClient:
    """
    Интерфейс клиента ML
    """
    def get_next_review(self, history: List[Dict]) -> Dict:
        raise NotImplementedError



class TextAnalyzer:
    #Заглушка ML

    def analyze(
        self,
        content: str
    ):
        words = content.split()
        total_words = len(words)
        unknown_words = int(
            total_words * random.uniform(0.1, 0.3)
        )

        difficulty = unknown_words / total_words

        if difficulty < 0.2:
            level = "A2"
        elif difficulty < 0.4:
            level = "B1"
        elif difficulty < 0.6:
            level = "B2"
        else:
            level = "C1"

        recommended = words[:5]
        return {
            "level": level,
            "unknown_words": unknown_words,
            "coveragepercent": difficulty*100,
            "recommended_words": recommended
        }

async def analyze_text(
    content: str
):
    analyzer = TextAnalyzer()
    result = analyzer.analyze(content)
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ML_SERVICE_URL}/analyze",
            json={
                "title": title,
                "content": content
            }
        )
    """
    return result
