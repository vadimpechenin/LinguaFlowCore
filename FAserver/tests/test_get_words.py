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

def test_get_words_auth_headers(client, auth_headers):
    res = client.get("/words", headers=auth_headers)

    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 1
