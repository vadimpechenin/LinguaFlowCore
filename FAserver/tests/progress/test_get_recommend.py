def test_get_recommend(client, auth_headers):
    data = {
               "refresh": False
           }
    res = client.post(
        "/review/words",
        json = data,
        headers=auth_headers,
    )

    assert res.status_code == 200
    data1 = res.json()

    assert isinstance(data1, list)
    assert len(data1) >= 1
    data = {
               "refresh": True
           }
    res = client.post(
        "/review/words",
        json=data,
        headers=auth_headers,
    )

    assert res.status_code == 200
    data2 = res.json()

    assert isinstance(data2, list)
    assert len(data2) >= 1
    assert(data1[0]['texten']!=data2[0]['texten'])
