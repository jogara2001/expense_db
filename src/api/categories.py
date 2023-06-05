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
    - `category_id`: the id of the category
    - `category_name`: the name of the category
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
    '''
    This endpoint provides the list of categories associated with a user
    '''
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
    '''
    This endpoint returns the details of a specific category
    '''
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
    '''
    This endpoint returns the percentage of a user's overall allocated budget
    on a per-category basis. Categories are ranked overall from 
    '''
    with db.engine.begin() as conn:
        budgets = conn.execute(sqlalchemy.text(
            '''
            SELECT c.category_name, b.budget_amount, 
            (b.budget_amount / total_budget.total_budget) * 100 AS budget_percentage
            FROM category AS c
            JOIN budget AS b ON b.category_id = c.category_id
            JOIN (SELECT SUM(budget_amount) AS total_budget FROM budget) 
            AS total_budget
            WHERE c.user_id = :user_id
            ORDER BY budget_percentage DESC;
            '''
        ), {'user_id': user_id}).fetchall()
    return [
        {
            "category_name": budget.category_name,
            "budget_amount": budget.budget_amount,
            "budget_percentage": budget.budget_percentage,
        } for budget in budgets
    ]
