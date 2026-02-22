def test_create_text(client, auth_headers):
    text_title="THE SECRET GARDEN"

    res = client.get(
        f"/texts/{text_title}",
        headers=auth_headers,
    )

    assert res.status_code == 200
    data = res.json()

    assert data["title"] == "THE SECRET GARDEN"




