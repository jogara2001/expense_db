from datetime import datetime, timezone
import uuid

from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)


def test_post_expense():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/",
        json=new_category
    )

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/",
        json=new_expense
    )

    assert expense_response.status_code == 200
    assert expense_response.json()["category_id"] == new_expense["category_id"]
    assert expense_response.json()["description"] == new_expense["description"]



def test_get_expense():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/",
        json=new_category
    )

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/",
        json=new_expense
    )
    expense_id = expense_response.json()["expense_id"]

    get_expense_response = client.get(
        f"/users/{user_id}/expenses/{expense_id}/"
    )

    assert get_expense_response.status_code == 200
    assert get_expense_response.json()["expense_id"] == expense_id
    assert get_expense_response.json(
    )["category"] == new_category["category_name"]
    assert get_expense_response.json(
    )["description"] == new_expense["description"]
    assert get_expense_response.json()["cost"] == 0.0

    new_item = {
        "name": "test_item",
        "cost": 25,
    }
    client.post(
        f"/users/{user_id}/expenses/{expense_id}/items",
        json=new_item
    )

    get_expense_response = client.get(
        f"/users/{user_id}/expenses/{expense_id}/"
    )

    assert get_expense_response.json()["cost"] == 25.0


def test_list_expense():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/categories/",
        json=new_category
    )

    new_expense_one = {
        "date_time": str(datetime.utcnow()).replace(" ", "T"),
        "category_id": category_response.json()["category_id"],
        "description": "string_1"
    }
    client.post(
        f"/users/{user_id}/expenses/",
        json=new_expense_one
    )

    new_expense_two = {
        "date_time": str(datetime.utcnow()).replace(" ", "T"),
        "category_id": category_response.json()["category_id"],
        "description": "string_2"
    }
    response_two = client.post(
        f"/users/{user_id}/expenses/",
        json=new_expense_two
    )

    new_expense_three = {
        "date_time": str(datetime.utcnow()).replace(" ", "T"),
        "category_id": category_response.json()["category_id"],
        "description": "string_3"
    }
    response_three = client.post(
        f"/users/{user_id}/expenses/",
        json=new_expense_three
    )

    list_expense_response = client.get(
        f"/users/{user_id}/expenses?limit=2&offset=1"
    )

    assert list_expense_response.status_code == 200
    assert len(list_expense_response.json()) == 2
    assert list_expense_response.json()[0]["expense_id"] == response_two.json()[
        "expense_id"]
    assert list_expense_response.json()[1]["expense_id"] == response_three.json()[
        "expense_id"]
    assert list_expense_response.json(
    )[0]["description"] == new_expense_two["description"]
    assert list_expense_response.json(
    )[1]["description"] == new_expense_three["description"]
