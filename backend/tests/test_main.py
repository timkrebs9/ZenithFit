from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    # assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "age": 30,
            "gender": "male",
            "email": "testuser@gmail.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["name"] == "Test User"
    assert data["data"]["age"] == 30
    assert data["data"]["gender"] == "male"
    assert data["data"]["email"] == "testuser@gmail.com"
    assert "id" in data["data"]


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["id"] == "1"


def test_update_user():
    response = client.put(
        "/users/1",
        json={
            "name": "Updated User",
            "age": 35,
            "gender": "female",
            "email": "updateduser@gmail.com",
            "password": "updatedpassword",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "Updated User"
    assert data["data"]["age"] == 35
    assert data["data"]["gender"] == "female"
    assert data["data"]["email"] == "updateduser@gmail.com"


def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 204
