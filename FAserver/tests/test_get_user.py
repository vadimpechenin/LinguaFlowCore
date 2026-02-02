def test_get_user(client):
    response = client.post("/auth/login/",
        json={
            "username": "test_user",
            "password": "sec23"},
                           )

    username = "test_user"
    response = client.get(f"/users/{username}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_user@example.com"

    response = client.get("/users/me")