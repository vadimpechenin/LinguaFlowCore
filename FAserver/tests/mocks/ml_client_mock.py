from typing import Set, Dict

from app.services.ml_client import MLClient, TextCoverageAnalyzer


class MockMLClient(MLClient):
    """

    """
    async def recommend(
            self,
            words
    ):
        # простая логика
        return [
            {
                "id": w.id,
                "texten": w.texten
            }
            for w in words[:5]
        ]

    async def analyze_text(
            self,
            content: str,
            user_words: Set[str]
    )-> Dict:
        analyzer = TextCoverageAnalyzer(user_words)
        result = analyzer.analyze(content)
        return result
