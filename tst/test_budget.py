import json
import random
from datetime import datetime, timedelta
import uuid

from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)


def test_create_budget():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/?password={new_user['password']}",
        json=new_category
    )
    category_id = category_response.json()["category_id"]

    new_budget = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response = client.post(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}",
        json=new_budget
    )
    start_format = datetime.fromisoformat(
        budget_response.json()["start_date"]).date()
    end_format = datetime.fromisoformat(
        budget_response.json()["end_date"]).date()

    assert budget_response.status_code == 200
    assert budget_response.json()["budget_id"] is not None
    assert budget_response.json()["budget"] == new_budget["budget"]
    assert budget_response.json()["category_id"] == category_id
    assert str(start_format) == new_budget["start_date"]
    assert str(end_format) == new_budget["end_date"]


def test_create_budget_wrong_password():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/?password={new_user['password']}",
        json=new_category
    )
    category_id = category_response.json()["category_id"]

    new_budget = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response = client.post(
        f"/users/{user_id}/categories/{category_id}/budget?password=wrong_password",
        json=new_budget
    )

    assert budget_response.status_code == 401


def test_get_budget():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/?password={new_user['password']}",
        json=new_category
    )
    category_id = category_response.json()["category_id"]

    new_budget = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response = client.post(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}",
        json=new_budget
    )
    budget_id = budget_response.json()["budget_id"]

    response = client.get(
        f"/users/{user_id}/categories/{category_id}/budget/{budget_id}"
        f"?password={new_user['password']}"
    )

    start_format = datetime.fromisoformat(
        response.json()["start_date"]).date()
    end_format = datetime.fromisoformat(response.json()["end_date"]).date()

    assert response.status_code == 200
    assert response.json()["budget_id"] == budget_id
    assert response.json()["budget"] == new_budget["budget"]
    assert str(start_format) == new_budget["start_date"]
    assert str(end_format) == new_budget["end_date"]
    assert response.json()["category_id"] == category_id


def test_get_budget_wrong_password():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/?password={new_user['password']}",
        json=new_category
    )
    category_id = category_response.json()["category_id"]

    new_budget = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response = client.post(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}",
        json=new_budget
    )
    budget_id = budget_response.json()["budget_id"]

    response = client.get(
        f"/users/{user_id}/categories/{category_id}/budget/{budget_id}"
        f"?password=wrong"
    )
    assert response.status_code == 401


def test_list_budget():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/?password={new_user['password']}",
        json=new_category
    )
    category_id = category_response.json()["category_id"]

    new_budget_one = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response_one = client.post(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}",
        json=new_budget_one
    )

    new_budget_two = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response_two = client.post(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}",
        json=new_budget_two
    )

    response = client.get(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}"
    )

    start_format_one = datetime.fromisoformat(
        response.json()[0]["start_date"]).date()
    end_format_one = datetime.fromisoformat(
        response.json()[0]["end_date"]).date()
    start_format_two = datetime.fromisoformat(
        response.json()[1]["start_date"]).date()
    end_format_two = datetime.fromisoformat(
        response.json()[1]["end_date"]).date()

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["budget_id"] == budget_response_one.json()[
        "budget_id"]
    assert response.json()[1]["budget_id"] == budget_response_two.json()[
        "budget_id"]
    assert response.json()[0]["category_name"] == new_category["category_name"]
    assert response.json()[1]["category_name"] == new_category["category_name"]
    assert response.json()[0]["amount_allocated"] == new_budget_one["budget"]
    assert response.json()[1]["amount_allocated"] == new_budget_two["budget"]
    assert str(start_format_one) == new_budget_one["start_date"]
    assert str(end_format_one) == new_budget_one["end_date"]
    assert str(start_format_two) == new_budget_two["start_date"]
    assert str(end_format_two) == new_budget_two["end_date"]


def test_list_budget_wrong_password():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/?password={new_user['password']}",
        json=new_category
    )
    category_id = category_response.json()["category_id"]

    new_budget_one = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response_one = client.post(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}",
        json=new_budget_one
    )

    new_budget_two = {
        "budget": random.randint(1, 1000),
        "start_date": str(datetime.utcnow().date()),
        "end_date": str(datetime.utcnow().date() + timedelta(days=7))
    }
    budget_response_two = client.post(
        f"/users/{user_id}/categories/{category_id}/budget"
        f"?password={new_user['password']}",
        json=new_budget_two
    )

    response = client.get(
        f"/users/{user_id}/categories/{category_id}/budget?password=wrong_password"
    )

    assert response.status_code == 401
