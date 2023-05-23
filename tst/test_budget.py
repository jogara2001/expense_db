# import json
# import random

# from fastapi.testclient import TestClient

# from src.api.server import app

# client = TestClient(app)

# BUDGET_TEST_USER = 13


# def test_get_budget():
#     response = client.get(f"/users/{BUDGET_TEST_USER}/budget/?budget_category_id=3")
#     assert response.status_code == 200

#     with open("tst/budget/13-budget-3.json", encoding="utf-8") as f:
#         assert response.json() == json.load(f)


# def test_get_budget_with_expenses():
#     response = client.get(f"/users/{BUDGET_TEST_USER}/budget/?budget_category_id=4")
#     assert response.status_code == 200

#     with open("tst/budget/13-budget-4.json", encoding="utf-8") as f:
#         assert response.json() == json.load(f)


# def test_set_budget_new():
#     budget_list_response = client.get(f"/users/{BUDGET_TEST_USER}/budget/")
#     num = len(budget_list_response.json())

#     inputJson = {
#         "budget": 100
#     }
#     post_response = client.post(
#         f"/users/{BUDGET_TEST_USER}/budget/NEW_BUDGET{num}/",
#         json=inputJson
#     )
#     assert post_response.status_code == 200

#     assert post_response.json()["category_name"] == f"NEW_BUDGET{num}"
#     assert post_response.json()["user_id"] == BUDGET_TEST_USER
#     assert post_response.json()["monthly_budget"] == 100


# def test_set_budget_update():
#     budget = random.Random().randint(a=0, b=1000)
#     inputJson = {
#         "budget": budget
#     }
#     post_response = client.post(
#         f"/users/{BUDGET_TEST_USER}/budget/TestBudgetUpdate/",
#         json=inputJson
#     )
#     assert post_response.status_code == 200
#     assert post_response.json() == {
#         "category_id": 5,
#         "category_name": "TestBudgetUpdate",
#         "user_id": 13,
#         "monthly_budget": budget
#     }
