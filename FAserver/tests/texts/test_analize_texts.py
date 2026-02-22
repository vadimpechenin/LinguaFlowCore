import os
from pathlib import Path


def test_create_text(client, auth_headers):
    text_title="THE SECRET GARDEN"

    res = client.post(
        f"/texts/{text_title}/analyze",
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert data["title"] == "THE SECRET GARDEN"
    assert len(data["recommended_words"]) > 4



