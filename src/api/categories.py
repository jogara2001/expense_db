import sqlalchemy
from fastapi import APIRouter
from pydantic import BaseModel

from src import database as db
from src.sql_utils import authenticate

router = APIRouter()


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
    authenticate(user_id, password)
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
