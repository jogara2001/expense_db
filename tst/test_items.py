import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)


def test_post_item():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)

    assert user_response.status_code == 200
    assert user_response.json()["name"] == new_user["name"]
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/category/?password={new_user['password']}",
        json=new_category
    )

    assert category_response.status_code == 200
    assert category_response.json(
    )["category_name"] == new_category["category_name"]

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/?password={new_user['password']}",
        json=new_expense
    )

    assert expense_response.status_code == 200
    assert expense_response.json()["category_id"] == new_expense["category_id"]
    expense_id = expense_response.json()["expense_id"]

    new_item = {
        "name": "test_item",
        "cost": 25,
    }
    item_response = client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item
    )

    assert item_response.status_code == 200
    assert item_response.json()["item_name"] == new_item["name"]
    assert item_response.json()["cost"] == new_item["cost"]


def test_post_item_wrong_password():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)

    assert user_response.status_code == 200
    assert user_response.json()["name"] == new_user["name"]
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/category/?password={new_user['password']}",
        json=new_category
    )

    assert category_response.status_code == 200
    assert category_response.json(
    )["category_name"] == new_category["category_name"]

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/?password={new_user['password']}",
        json=new_expense
    )

    assert expense_response.status_code == 200
    assert expense_response.json()["category_id"] == new_expense["category_id"]
    expense_id = expense_response.json()["expense_id"]

    new_item = {
        "name": "test_item",
        "cost": 25,
    }
    item_response = client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password=wrong",
        json=new_item
    )

    assert item_response.status_code == 401


def test_get_item():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)

    assert user_response.status_code == 200
    assert user_response.json()["name"] == new_user["name"]
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/category/?password={new_user['password']}",
        json=new_category
    )

    assert category_response.status_code == 200
    assert category_response.json(
    )["category_name"] == new_category["category_name"]

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/?password={new_user['password']}",
        json=new_expense
    )

    assert expense_response.status_code == 200
    assert expense_response.json()["category_id"] == new_expense["category_id"]
    expense_id = expense_response.json()["expense_id"]

    new_item = {
        "name": "test_item",
        "cost": 25,
    }
    item_response = client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item
    )

    assert item_response.status_code == 200
    assert item_response.json()["item_name"] == new_item["name"]
    assert item_response.json()["cost"] == new_item["cost"]
    item_id = item_response.json()["item_id"]

    item_get_response = client.get(
        f"/users/{user_id}/expenses/{expense_id}/items/{item_id}?password={new_user['password']}"
    )

    assert item_get_response.status_code == 200
    assert item_get_response.json()["item_id"] == item_response.json()[
        "item_id"]
    assert item_get_response.json()["item_name"] == new_item["name"]
    assert item_get_response.json()["cost"] == new_item["cost"]
    assert item_get_response.json()["expense_id"] == expense_id
    assert item_get_response.json()["user_id"] == user_id


def test_get_item_wrong_password():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)

    assert user_response.status_code == 200
    assert user_response.json()["name"] == new_user["name"]
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/category/?password={new_user['password']}",
        json=new_category
    )

    assert category_response.status_code == 200
    assert category_response.json(
    )["category_name"] == new_category["category_name"]

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/?password={new_user['password']}",
        json=new_expense
    )

    assert expense_response.status_code == 200
    assert expense_response.json()["category_id"] == new_expense["category_id"]
    expense_id = expense_response.json()["expense_id"]

    new_item = {
        "name": "test_item",
        "cost": 25,
    }
    item_response = client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item
    )

    assert item_response.status_code == 200
    assert item_response.json()["item_name"] == new_item["name"]
    assert item_response.json()["cost"] == new_item["cost"]
    item_id = item_response.json()["item_id"]

    item_get_response = client.get(
        f"/users/{user_id}/expenses/{expense_id}/items/{item_id}?password=wrong"
    )

    assert item_get_response.status_code == 401


def test_list_item():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/category/?password={new_user['password']}",
        json=new_category
    )

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/?password={new_user['password']}",
        json=new_expense
    )
    expense_id = expense_response.json()["expense_id"]

    new_item_one = {
        "name": "test_item_one",
        "cost": 5,
    }
    client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item_one
    )
    new_item_two = {
        "name": "test_item_two",
        "cost": 10,
    }
    client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item_two
    )
    new_item_three = {
        "name": "test_item_three",
        "cost": 15,
    }
    client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item_three
    )

    item_list_response = client.get(
        f"/users/{user_id}/expenses/{expense_id}/items"
        f"?password={new_user['password']}&limit=2&offset=1"
    )

    assert item_list_response.status_code == 200
    assert len(item_list_response.json()) == 2
    assert item_list_response.json()[0]["item_name"] == new_item_two["name"]
    assert item_list_response.json()[0]["cost"] == new_item_two["cost"]
    assert item_list_response.json()[1]["item_name"] == new_item_three["name"]
    assert item_list_response.json()[1]["cost"] == new_item_three["cost"]

def test_list_item_wrong_password():
    new_user = {
        "name": str(uuid.uuid4()),
        "password": "test_password",
    }
    user_response = client.post("/users/", json=new_user)
    user_id = user_response.json()["user_id"]

    new_category = {"category_name": "test_category"}
    category_response = client.post(
        f"/users/{user_id}/category/?password={new_user['password']}",
        json=new_category
    )

    new_expense = {
        "date_time": datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
        "category_id": category_response.json()["category_id"],
        "description": "string"
    }
    expense_response = client.post(
        f"/users/{user_id}/expenses/?password={new_user['password']}",
        json=new_expense
    )
    expense_id = expense_response.json()["expense_id"]

    new_item_one = {
        "name": "test_item_one",
        "cost": 5,
    }
    client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item_one
    )
    new_item_two = {
        "name": "test_item_two",
        "cost": 10,
    }
    client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item_two
    )
    new_item_three = {
        "name": "test_item_three",
        "cost": 15,
    }
    client.post(
        f"/users/{user_id}/expenses/{expense_id}/items?password={new_user['password']}",
        json=new_item_three
    )

    item_list_response = client.get(
        f"/users/{user_id}/expenses/{expense_id}/items"
        f"?password=wrong&limit=2&offset=1"
    )

    assert item_list_response.status_code == 401
