from app.services.ml_client import MLClient, TextAnalyzer


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
            content: str
    )-> dict:
        analyzer = TextAnalyzer()
        result = analyzer.analyze(content)
        return result
