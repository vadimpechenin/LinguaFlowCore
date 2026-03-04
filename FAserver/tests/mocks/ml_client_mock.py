from typing import Set, Dict, List

from app.services.ml_client import MLClient
from app.services.pipelines.text_analyzer import TextAnalyzer
from app.services.pipelines.word_analyzer import WordAnalyzer


class MockMLClient(MLClient):
    """

    """
    async def recommend(
            self,
            words, limit: int
    ):
        analyzer =WordAnalyzer()
        result = analyzer.recommend(words,limit)
        # простая логика
        return result


    async def get_new_words(self, base_words: List[str], new_words: List[str]) -> List[str]:
        # простая логика
        analyzer = WordAnalyzer()
        result = analyzer.get_unknown_words(base_words, new_words)
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