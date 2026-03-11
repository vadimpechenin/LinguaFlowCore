def test_get_user(client):
    response = client.post("/auth/login/",
        json={
            "username": "test_user",
            "password": "sec23"},
                           )
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]

    response = client.get("/users/me2",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"

    response = client.get("/users/me", headers = {"Authorization":f"Bearer{token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"