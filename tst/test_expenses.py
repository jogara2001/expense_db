import json
from datetime import datetime

from fastapi.testclient import TestClient

from src.api.server import app

client = TestClient(app)

EXPENSE_TEST_USER = 26
EXPENSE_TEST_USER_POSTS = 29

def test_get_expense():
    response = client.get(f"/user/{EXPENSE_TEST_USER}/expense/5")
    assert response.status_code == 200

    with open("tst/expenses/26-expenses-5.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_expense_error():
    response = client.get(f"/user/{EXPENSE_TEST_USER}/expense/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "expense not found."}


def test_list_expenses():
    # sample for list_expense : /user/{user_id}/expenses
    response = client.get(
        f"/user/{EXPENSE_TEST_USER}/expenses?start_date=2023-05-1%2001%3A05%3A29&end_date=2023-05-10%2001%3A05%3A29")
    assert response.status_code == 200

    with open("tst/expenses/26-expenses-list.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_list_expenses_error():
    response = client.get("/user/999999/expense/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found."}


def test_add_expense_new():
    data = {
      "cost": 25,
      "date_time": "2023-05-08 14:19:45",
      "category_id": 16,
      "description": "string"
    }

    post_response = client.post(
        f"/user/{EXPENSE_TEST_USER_POSTS}/expense/",
        json=data
    )
    assert post_response.status_code == 200
    assert post_response.json()["category_id"] == data["category_id"]
    assert post_response.json()["date_time"] == data["date_time"]
    assert post_response.json()["cost"] == data["cost"]
    assert post_response.json()["description"] == data["description"]
    expense_id = post_response.json()["expense_id"]
    dt = datetime.strptime(data["date_time"], '%Y-%m-%d %H:%M:%S')
    formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    response = client.get(f"/user/{EXPENSE_TEST_USER_POSTS}/expense/{expense_id}")
    assert response.status_code == 200
    assert response.json()["expense_id"] == expense_id
    assert response.json()["date_time"] == formatted_dt
    assert response.json()["cost"] == data["cost"]
    assert response.json()["description"] == data["description"]

def test_add_expense_error():
    data = {
      "cost": 25,
      "date_time": "2023-05-08 14:19:45",
      "category_id": 999999999,
      "description": "string"
    }

    post_response = client.post(
        f"/user/{EXPENSE_TEST_USER_POSTS}/expense/",
        json=data
    )
    assert post_response.status_code == 404
    assert post_response.json() == {"detail": "budget category not found."}
