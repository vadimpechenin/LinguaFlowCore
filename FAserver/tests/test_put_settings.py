def test_put_settings_auth_headers(client, auth_headers):
    res = client.put("/user-settings",
        json={
            "createdat": None,
            "learninglanguage": "en",
            "preferredvoice": "ru",
            "dailywordlimit": 10,
            "enableaudio": None,
            "enablenotifications": False,
            "timezone": None
        }, headers=auth_headers)

    assert res.status_code == 200
    assert res.json()==True