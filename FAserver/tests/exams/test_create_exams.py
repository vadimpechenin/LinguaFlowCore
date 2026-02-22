def test_create_exam(client, auth_headers):
    payload = {
        "title": "A1 Vocabulary Test",
        "difficultylevel": "A1",
        "score": 0,
    }

    res = client.post(
        "/exams/start",
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert data["title"] == "A1 Vocabulary Test"
    #assert len(data["questions"]) <= 5



