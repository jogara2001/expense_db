import datetime
import uuid

from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)


def test_list_deposit():
    name = str(uuid.uuid4())
    password = "password"
    data1 = {
        "name": name,
        "password": password
    }

    postResponse = client.post("/users/", json=data1)
    assert postResponse.status_code == 200
    user_id = postResponse.json()["user_id"]

    timestamp = str(datetime.datetime.utcnow()).replace(" ", "T")
    data2 = {
        "amount": 100,
        "timestamp": timestamp
    }

    postResponse = client.post(f"/user/{user_id}/deposits/?password={password}", json=data2)
    assert postResponse.status_code == 200

    response = client.get(
        f"/user/{user_id}/deposits/?password={password}"
        f"&limit=1&offset=0")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["amount"] == 100
    assert response.json()[0]["timestamp"] == timestamp


def test_list_deposit2():
    name = str(uuid.uuid4())
    password = "password"
    data1 = {
        "name": name,
        "password": password
    }

    postResponse = client.post("/users/", json=data1)
    assert postResponse.status_code == 200
    user_id = postResponse.json()["user_id"]

    response = client.get(
        f"/user/{user_id}/deposits/?password={password}"
        f"&limit=1&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_post_deposit():
    name = str(uuid.uuid4())
    password = "password"
    data1 = {
        "name": name,
        "password": password
    }

    postResponse = client.post("/users/", json=data1)
    assert postResponse.status_code == 200
    user_id = postResponse.json()["user_id"]

    timestamp = str(datetime.datetime.utcnow()).replace(" ", "T")
    data2 = {
        "amount": 100,
        "timestamp": timestamp
    }

    postResponse = client.post(f"/user/{user_id}/deposits/?password={password}", json=data2)
    assert postResponse.status_code == 200
    assert postResponse.json()["user_id"] == user_id
    assert postResponse.json()["amount"] == 100
    assert postResponse.json()["timestamp"] == timestamp
