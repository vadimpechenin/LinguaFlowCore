def test_get_recommend(client, auth_headers):
    #Получение рекомендаций, имитация их изучения и ответ на сервер
    res = client.get(
        "/review/words",
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    for word in data:
        payload = {
            "wordid": word["id"],
            "iscorrect": True
        }
        answer = client.post(
            "/review/answer",
            json=payload,
            headers=auth_headers,
        )
        assert answer.status_code == 200
        data = answer.json()
        assert data["isknown"] == True



