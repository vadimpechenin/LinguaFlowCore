import requests
from app.core import settings

from app.services.ml_client import MLClient


class MLClientIml(MLClient):
    def get_next_review(self, history):
        resp = requests.post(
            f"{settings.ML_SERVICE_URL}/review/next",
            json={"history": history},
            timeout=2,
        )
        resp.raise_for_status()
        return resp.json()
