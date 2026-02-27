def test_get_list_words_progress(client, auth_headers):
    # получаем список слов
    words = client.get("/words/", headers=auth_headers).json()
    word_ids=[]
    for word in words:
        word_ids.append(word["id"])
    review_response = client.post(
        f"/review/progress",
        json={
            "word_ids": word_ids,
            "is_known": False
        }, headers=auth_headers
    )

    assert review_response.status_code == 200
    assert review_response.json()["progress_created"] >20
    assert review_response.json()["features_created"] >20