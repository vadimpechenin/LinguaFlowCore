def test_create_words(client, auth_headers):
    # добавляем слова
    words = [
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

    for word in words:
        response = client.post("/words", json=word, headers=auth_headers)
        assert response.status_code == 200