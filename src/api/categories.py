import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src import database as db
from src import sql_utils as utils

router = APIRouter()

@router.get("/user/{user_id}/categories", tags=["category"])
def get_user_categories(user_id: int, password: str):
    '''
    This endpoint provides the list of categories associated with a user
    '''
    utils.authenticate(user_id, password)
    with db.engine.connect() as conn:
        categories = conn.execute(sqlalchemy.text(
            '''
            SELECT category_name FROM category AS c
            JOIN "user" AS u ON u.user_id = c.user_id
            WHERE u.user_id = :user_id
            ORDER BY category_name ASC
            '''
        ), {'user_id': user_id}).fetchall()
    return [
        {"category name": category.category_name} for category in categories
    ]

class CategoryJson(BaseModel):
    category_name: str

@router.post("/users/{user_id}/category/", tags=["category"])
def create_category(user_id: int, password: str, category_json: CategoryJson):
    """
    This endpoint creates a new category for a specific user.

    - `user_id`: the id of the user
    - `category_id`: the id of the category
    - `category_name`: the name of the category
    """
    utils.authenticate(user_id, password)
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
        "category_name": category_data.name,
        "user_id": category_data.user_id,
    }
 
@router.get("/users/{user_id}/category/budgets", tags=["category"])
def category_budget_percentage(user_id: int, password: str):
    '''
    This endpoint returns the percentage of a user's overall allocated budget
    on a per-category basis. Categories are ranked overall from 
    '''
    utils.authenticate(user_id, password)
    with db.engine.begin() as conn:
        category_sums = conn.execute(sqlalchemy.text('''
        SELECT COALESCE(SUM(budget),0.0) sums, category_name FROM category as c
        JOIN budget AS b ON b.category_id = c.category_id
        WHERE c.user_id = :user_id
        GROUP BY category_name
        '''), {"user_id": user_id})
    net_sum = sum([c_sum.sums for c_sum in category_sums])
    return [
        {
            "category_name": c_sum.category_name,
            "budget_percent" : str(round(c_sum.sums / net_sum * 100,2))+"%"
        } for c_sum in category_sums
    ] 
