import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src import database as db

router = APIRouter()

class CategoryJson(BaseModel):
    category_name: str


@router.post("/users/{user_id}/categories/", tags=["category"])
def create_category(user_id: int, category_json: CategoryJson):
    """
    This endpoint creates a new category for a specific user.

    - `user_id`: the id of the user
    - `category_json`: object consisting of the following
        - `category_name`: the name of the category to create
    """
    with db.engine.begin() as conn:
        category_data = conn.execute(
            sqlalchemy.text('''
            INSERT INTO category (category_name, user_id)
            VALUES (:category_name, :user_id)
            RETURNING category_id, category_name, user_id;
            '''),
            {"category_name": category_json.category_name, "user_id": user_id}
        ).fetchone()
    return {
        "category_id": category_data.category_id,
        "category_name": category_data.category_name,
        "user_id": category_data.user_id,
    }


@router.get("/users/{user_id}/categories", tags=["category"])
def list_categories(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
):
    """
    This endpoint provides the list of categories associated with a user

    - `user_id`: the id of the associated user
    - `limit`: the maximum number of results to return
    - `offset`: the number of results to skip

    """
    with db.engine.connect() as conn:
        categories = conn.execute(sqlalchemy.text(
            '''
            SELECT category_name, category_id FROM category AS c
            JOIN "user" AS u ON u.user_id = c.user_id
            WHERE u.user_id = :user_id
            LIMIT :limit
            OFFSET :offset
            '''
        ), {"user_id": user_id, "limit": limit, "offset": offset}).fetchall()
    return [
        {
            "category_name": category.category_name,
            "category_id": category.category_id,
            "user_id": user_id,
        } for category in categories
    ]


@router.get("/users/{user_id}/categories/{category_id}", tags=["category"])
def get_category(
    user_id: int,
    category_id: int,
):
    """
    This endpoint returns the details of a specific category

    - `user_id`: the id of the user associated with the category
    - `category_id`: the id of the category to get
    """
    with db.engine.connect() as conn:
        category = conn.execute(sqlalchemy.text(
            '''
            SELECT category_name, category_id FROM category AS c
            JOIN "user" AS u ON u.user_id = c.user_id
            WHERE u.user_id = :user_id
            AND c.category_id = :category_id
            '''
        ), {"user_id": user_id, "category_id": category_id}).fetchone()
        if category is None:
            raise HTTPException(status_code=404, detail="category not found.")
    return {
        "category_name": category.category_name,
        "category_id": category.category_id,
        "user_id": user_id,
    }


@router.get("/users/{user_id}/category/budgets", tags=["category"])
def category_budget_percentage(user_id: int):
    """
    This endpoint returns the percentage of a user's overall allocated budget
    on a per-category basis. Categories are ranked overall by percentage descending

    - `user_id`: the associated user
    """
    with db.engine.begin() as conn:
        budgets = conn.execute(sqlalchemy.text(
            '''
            SELECT COALESCE(SUM(budget),0.0) sums, category_name FROM category as c
            LEFT JOIN budget AS b ON b.category_id = c.category_id
            WHERE c.user_id = :user_id
            GROUP BY category_name
            '''
        ), {'user_id': user_id}).fetchall()
    net_sum = sum([c_sum.sums for c_sum in budgets])
    return [
        {
            "category_name": budget.category_name,
            "budget_amount": budget.sums,
            "budget_percentage": str(round(budget.sums/net_sum * 100,2))+"%",
        } for budget in budgets
    ]
