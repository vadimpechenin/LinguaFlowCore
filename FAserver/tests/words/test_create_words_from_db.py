import pandas as pd

from app.core.settings import EXCEL_WORDS_PATH, SHEET_NAME, REQUIRED_COLUMNS


def test_create_words_from_db(client, auth_headers):
    # Загружаем слова из базы, которых нет у пользователя
    response = client.get("/words/available", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    words = response.json()

    word_ids = []
    for item in words[0:2]:
        word_ids.append({"id": item["id"]})

    response = client.post("/words/add-to-progress", json=word_ids, headers=auth_headers)
    g = 0
