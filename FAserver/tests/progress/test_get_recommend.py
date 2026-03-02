def test_get_recommend(client, auth_headers):

    res = client.get(
        "/review/words",
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert isinstance(data, list)
    assert len(data) >= 1
