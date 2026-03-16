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

    assert isinstance(data1, dict)
    assert len(data1["words"]) >= 1
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

    assert isinstance(data2, dict)
    assert len(data2["words"]) >= 1
    #assert(data1["words"][0]['texten']==data2["words"][0]['texten'])
    assert(data1['was_refreshed']!=data2['was_refreshed'])