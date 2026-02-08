def test_post_exams(client):
    # 1️⃣ добавляем слова
    exam = [
        {
            "texten": "apple",
            "transcription": "ˈæp.əl",
            "textl": "яблоко",
            "partofspeech": "noun",
            "examplesentence": "I eat an apple.",
            "difficultylevel": "A1",
        },
        {
            "texten": "knowledge",
            "transcription": "ˈnɒlɪdʒ",
            "textl": "знание",
            "partofspeech": "noun",
            "examplesentence": "Knowledge is power.",
            "difficultylevel": "B1",
        },
    ]

    response = client.post("/exam/start", json=exam)
    assert response.status_code == 200