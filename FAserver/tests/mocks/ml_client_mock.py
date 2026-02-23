from app.services.ml_client import MLClient


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
