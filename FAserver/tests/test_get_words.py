def test_get_words(client):
       # 2️⃣ получаем список слов
    response = client.get("/words/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    text_ens = [w["texten"] for w in data]
    assert "apple" in text_ens
    assert "knowledge" in text_ens
