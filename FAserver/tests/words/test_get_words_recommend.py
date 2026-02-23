def test_get_words_recommend(client, auth_headers):
    response = client.get("/words/recommend", headers = auth_headers)#
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
