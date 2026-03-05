def test_create_exam(client, auth_headers):
    setings = client.get("/user-settings", headers=auth_headers).json()
    payload = {
        "difficultylevel": "B2",
        "size": setings['dailywordlimit']*2,
    }

    res = client.post(
        "/exams/start",
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert len(data["questions"] )== 20
    #assert len(data["questions"]) <= 5



