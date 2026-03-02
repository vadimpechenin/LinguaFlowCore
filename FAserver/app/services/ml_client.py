from typing import List, Dict, Set
import httpx
import random

from app.core.settings import ML_SERVICE_URL
from app.db.models.word import Word
from app.services.pipelines.text_analyzer import TextAnalyzer
from app.services.pipelines.word_analyzer import WordAnalyzer


async def recommend(
    user_id,
    words
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ML_SERVICE_URL}/recommend",
                json={
                    "user_id": user_id,
                    "words": words
                }
            )

            return response.json()

    except Exception:

        return {"words": []}


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
    async def recommend(self, words: List[Word], limit: int) -> List[dict]:
        raise NotImplementedError

    async def analyze_text(self,
            content: str, user_words: Set[str]) -> Dict:
        raise NotImplementedError

class MLClientIml(MLClient):
    """
    Реализация
    """
    async def recommend(
            self,
            words: List[Word], limit: int
    ) -> List[dict]:
        # простая логика
        analyzer = WordAnalyzer()
        result = analyzer.recommend(words,limit)
        # простая логика
        return result

    async def analyze_text(
            self,
            content: str,
            user_words: Set[str]
    )-> Dict:
        analyzer = TextAnalyzer(user_words)
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


def get_ml_client() -> MLClient:
    print("Зашел в get_ml_client")
    return MLClientIml()




