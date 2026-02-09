from app.services.ml_client import MLClient
from datetime import datetime, timedelta

class MockMLClient(MLClient):

    def get_next_review(self, history):
        return {
            "next_review_at": (
                datetime.utcnow() + timedelta(days=1)
            ).isoformat(),
            "difficulty": "A1",
            "confidence": 0.95,
        }
