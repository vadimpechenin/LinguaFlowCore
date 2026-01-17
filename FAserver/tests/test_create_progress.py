def test_get_progress(client):
    user_id = "b83618b2915447688156f1106b7be703"
    word_id = "24b11a1f499d4f449be2d191da4febf1"
    review_response = client.post(
        f"/review/{user_id}/{word_id}",
        json={
            "is_correct": True,
            "response_time_ms": 1000
        },
    )

    assert review_response.status_code == 200
    assert review_response.json() == {"status": "ok"}