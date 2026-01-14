def test_get_user(client):
    username = "administrator"
    response = client.get(f"/users/{username}")

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "kyz@mail.ru"