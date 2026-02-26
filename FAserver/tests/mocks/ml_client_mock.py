from typing import Set, Dict

from app.services.ml_client import MLClient, TextAnalyzer
from app.services.pipelines.text_analyzer import WordAnalyzer


class MockMLClient(MLClient):
    """

    """
    async def recommend(
            self,
            words
    ):
        analyzer =WordAnalyzer()
        result = analyzer.recommend(words[:100])
        # простая логика
        return result

    async def analyze_text(
            self,
            content: str,
            user_words: Set[str]
    )-> Dict:
        analyzer = TextAnalyzer(user_words)
        result = analyzer.analyze(content)
        return result
