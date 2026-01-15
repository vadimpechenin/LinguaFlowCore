def test_get_user(client):
    username = "test_user"
    response = client.get(f"/users/{username}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_user@example.com"