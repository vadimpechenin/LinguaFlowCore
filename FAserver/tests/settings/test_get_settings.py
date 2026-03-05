def test_get_settings_auth_headers(client, auth_headers):
    res = client.get("/user-settings", headers=auth_headers)

    assert res.status_code == 200
    assert isinstance(res.json(), dict)
    assert res.json()["createdat"] == 'ru'