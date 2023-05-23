import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)


def test_create_category():
    name = str(uuid.uuid4())
    password = "password"
    data = {
        "name": name,
        "password": password
    }

    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    data = {
        "category_name": "test_category"
    }

    response = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data)
    assert response.status_code == 200
    assert response.json()["category_id"] is not None
    assert response.json()["category_name"] == "test_category"


def test_create_category_wrong_password():
    name = str(uuid.uuid4())
    password = "password"
    data = {
        "name": name,
        "password": password
    }

    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    data = {
        "category_name": "test_category"
    }

    response = client.post(
        f"/users/{user_id}/categories/?password=wrong_password", json=data)
    assert response.status_code == 401


def test_list_categories():
    name = str(uuid.uuid4())
    password = "password"
    data = {
        "name": name,
        "password": password
    }

    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    data_one = {
        "category_name": "test_category"
    }

    response_one = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_one)
    assert response_one.status_code == 200

    data_two = {
        "category_name": "test_category_two"
    }
    response_two = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_two)
    assert response_two.status_code == 200
    
    data_three = {
        "category_name": "test_category_three"
    }
    response_three = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_three)
    assert response_three.status_code == 200

    list_response = client.get(f"/users/{user_id}/categories?password={password}")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 3

    list_response = client.get(
        f"/users/{user_id}/categories?password={password}"
        f"&limit=2&offset=1")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 2
    assert list_response.json()[0]["category_name"] == "test_category_two"
    assert list_response.json()[1]["category_name"] == "test_category_three"


def test_list_categories_wrong_password():
    name = str(uuid.uuid4())
    password = "password"
    data = {
        "name": name,
        "password": password
    }

    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    data_one = {
        "category_name": "test_category"
    }

    response_one = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_one)
    assert response_one.status_code == 200

    data_two = {
        "category_name": "test_category_two"
    }
    response_two = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_two)
    assert response_two.status_code == 200
    
    data_three = {
        "category_name": "test_category_three"
    }
    response_three = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_three)
    assert response_three.status_code == 200

    list_response = client.get(f"/users/{user_id}/categories?password=wrong_password")
    assert list_response.status_code == 401


def test_get_category():
    name = str(uuid.uuid4())
    password = "password"
    data = {
        "name": name,
        "password": password
    }

    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    data_one = {
        "category_name": "test_category"
    }

    response_one = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_one)
    assert response_one.status_code == 200
    category_id = response_one.json()["category_id"]

    get_response = client.get(
        f"/users/{user_id}/categories/{category_id}/?password={password}")
    assert get_response.status_code == 200
    assert get_response.json()["category_name"] == "test_category"


def test_get_category_wrong_password():
    name = str(uuid.uuid4())
    password = "password"
    data = {
        "name": name,
        "password": password
    }

    response = client.post("/users/", json=data)
    assert response.status_code == 200
    user_id = response.json()["user_id"]

    data_one = {
        "category_name": "test_category"
    }

    response_one = client.post(
        f"/users/{user_id}/categories/?password={password}", json=data_one)
    assert response_one.status_code == 200
    category_id = response_one.json()["category_id"]

    get_response = client.get(
        f"/users/{user_id}/categories/{category_id}/?password=wrong_password")
    assert get_response.status_code == 401
