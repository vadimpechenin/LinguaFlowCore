import random


def test_submit_exam(client, auth_headers):
    exams = client.get("/exams", headers=auth_headers).json()
    exam_id = exams[0]["id"]

    response = client.get("/words/")

    assert response.status_code == 200

    data = response.json()

    random.shuffle(data)
    words = data[:20]
    answers = [True, False]
    payload = {
        "answers": [
            {"word_id": q["id"], "is_correct": random.choice(answers)}
            for q in words
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