def test_get_words_auth_recommend(client, auth_headers):
    res = client.get("/words/recommend", headers=auth_headers)

    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) >= 1
