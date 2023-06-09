import uuid

from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)


def test_users():
    response = client.get("/users/")
    assert response.status_code == 200


def test_users_by_id():
    name = str(uuid.uuid4())
    password = "password"
    data = {
        "name": name,
        "password": password
    }

    postResponse = client.post("/users/", json=data)
    assert postResponse.status_code == 200
    user_id = postResponse.json()["user_id"]

    response = client.get(f"/users/{user_id}/")
    assert response.status_code == 200
    assert response.json() == {"user_id": user_id, "name": name, "balance": 0}


def test_users_by_id2():
    response = client.get("/users/99999999999/")
    assert response.status_code == 404


def test_list_users():
    name = str(uuid.uuid4())
    data = {
        "name": name,
        "password": "test"
    }

    postResponse = client.post("/users/", json=data)
    assert postResponse.status_code == 200
    user_id = postResponse.json()["user_id"]

    response = client.get(f"/users/?name={name}&limit=1&offset=0")
    assert response.status_code == 200
    assert response.json() == [{"user_id": user_id, "name": name}]


def test_basic_user_post():
    name = str(uuid.uuid4())
    data = {
        "name": name,
        "password": "test"
    }

    postResponse = client.post("/users/", json=data)
    assert postResponse.status_code == 200
    assert "user_id" in postResponse.json()
    assert postResponse.json()["name"] == name
