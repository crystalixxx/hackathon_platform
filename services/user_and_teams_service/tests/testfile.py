async def test_get_users(client):
    response = client.get("api/v0/user/")
    assert response.status_code == 200
