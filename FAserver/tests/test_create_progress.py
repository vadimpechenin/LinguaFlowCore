def test_get_progress(client, auth_headers):
    # получаем слово
    words = client.get("/words", headers=auth_headers).json()
    word_id = words[0]["id"]
    username = "test_user"
    user_id = client.get(f"/users/{username}").json()["id"]
    review_response = client.post(
        f"/review/{user_id}/{word_id}",
        json={
            "is_correct": True,
            "response_time_ms": 1000
        },
    )

    assert review_response.status_code == 200
    assert review_response.json() == {"status": "ok"}