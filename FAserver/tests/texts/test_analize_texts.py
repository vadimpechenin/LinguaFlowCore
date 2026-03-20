import os
from pathlib import Path


def test_create_text(client, auth_headers):
    text_title="THE SECRET GARDEN"
    text_title = "The Whispering Monolith"

    res = client.post(
        "/texts/analyze",
        json ={
            "title": text_title
        },
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert data["title"] == text_title
    assert len(data["recommended_words"]) > 4



