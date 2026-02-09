def test_post_progress(client, auth_headers):
    # получаем слово
    words = client.get("/words", headers=auth_headers).json()
    word_id = words[0]["id"]
    username = "test_user"
    client_id = client.get(f"/users/{username}").json()["id"]
    payload = {
        "client_id": client_id,
        "word_id": word_id,
        "is_correct": True,
        "response_time_ms": 1200,
    }

    res = client.post(
        "/review/progress",
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert data["word_id"] == word_id
    assert data["is_correct"] is True


def test_get_progress(client, auth_headers):
    res = client.get("/progress", headers=auth_headers)

    assert res.status_code == 200
    assert isinstance(res.json(), list)
