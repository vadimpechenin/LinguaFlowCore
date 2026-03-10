def test_create_user(client):
    create_response = client.post(
        "/auth/register/",
        json={
            "name": "Test2",
            "username": "test_user2",
            "email": "test_user2@example.com",
            "password": "sec233",
            "initiallevel": "A2",
        },
    )

    assert create_response.status_code == 200
    token_json = create_response.json()
    token = token_json["access_token"]
    assert len(token)>2
