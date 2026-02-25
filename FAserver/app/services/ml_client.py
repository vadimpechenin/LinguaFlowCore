from typing import List, Dict, Set
import httpx
import random

from app.core.settings import ML_SERVICE_URL
from app.db.models.word import Word
from app.services.pipelines.text_analyzer import WordAnalyzer


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
    async def recommend(self, words: List[Word]) -> List[dict]:
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
            words: List[Word]
    ) -> List[dict]:
        # простая логика

        return [
            {
                "id": w.id,
                "texten": w.texten
            }
            for w in words[:10]
        ]

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


import re
import spacy

nlp = spacy.load("en_core_web_sm")

class TextAnalyzer:
    """
    Text
    ↓
    Tokenizer
    ↓
    BERT encoder
    ↓
    CEFR classifier
    ↓
    Recommendation engine
    ↓
    Response
    """
    def __init__(self, user_words: Set[str]):
        # приводим к lowercase
        self.user_words = set(
            word.lower()
            for word in user_words
        )
        self.word_analyzer = WordAnalyzer()


    def preprocess_text(
            self,
            text: str
    ) -> Set[str]:
        # извлекаем только слова - базовая версия
        words = re.findall(
            r"[a-zA-Z']+",
            text.lower()

        )
        return set(words)

    def preprocess_text_nlp(self,text):
        #Улучшенная версия
        # с лемматизацией; частотным анализом
        doc = nlp(text)

        return set(
            token.lemma_
            for token in doc
            if token.is_alpha
        )

    def analyze(
            self,
            text: str
        ) -> Dict:
        #text_words = self.preprocess_text(text)
        text_words = self.preprocess_text_nlp(text)
        #Уровни сложности слов, пока не используем
        #result = self.word_analyzer.analyze(list(text_words))
        known = text_words.intersection(
            self.user_words
        )

        unknown = text_words.difference(
            self.user_words
        )

        total = len(text_words)
        known_count = len(known)
        unknown_count = len(unknown)

        coverage = (
            known_count / total * 100
            if total > 0 else 0
        )
        #TODO заглушки
        if coverage < 20:
            level = "C1"
        elif coverage < 40:
            level = "B2"
        elif coverage < 60:
            level = "B1"
        else:
            level = "A2"

        recommended = sorted(list(unknown)[:5])

        return {
            "total_words": total,
            "known_words": known_count,
            "unknown_words": unknown_count,
            "coverage_percent": round(coverage, 2),
            "recommended_words_list": recommended,
            "level": level
        }

