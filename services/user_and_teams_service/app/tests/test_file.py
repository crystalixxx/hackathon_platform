def test_create_user(client, connection_test):
    response = client.get("/api/v0/user/")
    assert response.status_code == 200
    assert response.json() == []

    user = {
        "email": "test@gmail.com",
        "first_name": "Oleg",
        "second_name": "Hello",
        "password": "123456789isnotagoodpassword",
        "role": "User",
    }
    response = client.post("/api/v0/user/")

    assert response.status_code == 200

    response = client.get("/api/v0/user/")
    assert response.status_code == 200

    assert len(response.json()) == 1
