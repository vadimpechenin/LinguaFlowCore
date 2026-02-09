def test_submit_exam(client, auth_headers):
    exams = client.get("/exams", headers=auth_headers).json()
    exam_id = exams[0]["id"]

    payload = {
        "answers": [
            {"word_id": q["word_id"], "is_correct": True}
            for q in exams[0]["questions"]
        ]
    }

    res = client.post(
        f"/exams/{exam_id}/submit",
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert "score" in data
    assert data["score"] >= 0