def test_get_user(client):
    create_response = client.post(
        "/users/",
        json={
            "name": "Test",
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "sec23",
            "initiallevel": "A1",
        },
    )

    assert create_response.status_code == 200
    user = create_response.json()
    user_name = user["username"]

    response = client.get(f"/users/{user_name}")

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == user_name
    assert data["email"] == "test_user@example.com"
    assert "createdat" in data