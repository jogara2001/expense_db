import sqlalchemy
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException

from src import database as db
from src.sql_utils import authenticate

router = APIRouter()


@router.get("/users/{user_id}/expenses/{expense_id}/items/{item_id}", tags=["items"])
def get_item(user_id: int, expense_id: int, item_id: int, password: str):
    """
    This endpoint returns the information for a specific item associated with a specific expense for a specific user.

    - `user_id`: the id of the user
    - `expense_id`: the id of the expense
    - `item_id`: the id of the item
    - `item_name`: the name of the item
    - `cost`: the monetary value of the item, in dollars
    """
    authenticate(user_id, password)
    with db.engine.connect() as conn:
        item_data = conn.execute(
            sqlalchemy.text('''
            SELECT item_id, name, cost
            FROM item
            INNER JOIN expense
            ON item.expense_id = expense.expense_id
            INNER JOIN category
            ON expense.category_id = category.category_id
            WHERE item.item_id = :item_id
            AND category.user_id = :user_id
            AND expense.expense_id = :expense_id;
            '''),
            {"item_id": item_id, "expense_id": expense_id, "user_id": user_id}
        ).fetchone()
        if not item_data:
            raise HTTPException(status_code=404, detail="item not found.")
    return {
        "item_id": item_data.item_id,
        "item_name": item_data.name,
        "cost": item_data.cost,
        "expense_id": expense_id,
        "user_id": user_id,
    }


@router.get("/users/{user_id}/expenses/{expense_id}/items", tags=["items"])
def list_items(user_id: int, expense_id: int, password: str, limit: int = 10, offset: int = 0):
    """
    This endpoint returns the information for all items associated with a specific expense for a specific user.

    - `user_id`: the id of the user
    - `expense_id`: the id of the expense
    - `item_id`: the id of the item
    - `item_name`: the name of the item
    - `cost`: the monetary value of the item, in dollars
    """
    authenticate(user_id, password)
    with db.engine.connect() as conn:
        item_data = conn.execute(
            sqlalchemy.text('''
            SELECT item_id, name, cost
            FROM item
            INNER JOIN expense
            ON item.expense_id = expense.expense_id
            INNER JOIN category
            ON expense.category_id = category.category_id
            WHERE expense.expense_id = :expense_id
            AND category.user_id = :user_id
            LIMIT :limit
            OFFSET :offset;
            '''),
            {"expense_id": expense_id, "user_id": user_id,
                "limit": limit, "offset": offset}
        ).fetchall()
    return [
        {
            "item_id": item.item_id,
            "item_name": item.name,
            "cost": item.cost,
            "expense_id": expense_id,
            "user_id": user_id,
        }
        for item in item_data
    ]

class ItemJson(BaseModel):
    cost: int
    name: str

@router.post("/users/{user_id}/expenses/{expense_id}/items", tags=["items"])
def create_item(user_id: int, expense_id: int, password: str, item_json: ItemJson):
    """
    This endpoint creates a new item associated with a specific expense for a specific user.

    The columns that the item table has are:
    - `item_id`: the id of the item
    - `expense_id`: the id of the expense
    - `cost`: the monetary value of the item, in dollars
    - `name`: the name of the item
    """
    authenticate(user_id, password)
    with db.engine.begin() as conn:
        expense = conn.execute(
            sqlalchemy.text('''
            SELECT expense_id
            FROM expense
            INNER JOIN category
            ON expense.category_id = category.category_id
            WHERE expense.expense_id = :expense_id
            AND category.user_id = :user_id;
            '''),
            {"expense_id": expense_id, "user_id": user_id}
        ).fetchone()
        if not expense:
            raise HTTPException(status_code=404, detail="expense not found.")

        inserted_item = conn.execute(
            sqlalchemy.text('''
            INSERT INTO item (expense_id, cost, name)
            VALUES (:expense_id, :cost, :name)
            RETURNING item_id;
            '''),
            {"expense_id": expense_id, "cost": item_json.cost, "name": item_json.name}
        )
    item = inserted_item.fetchone()
    return {
        "item_id": item.item_id,
        "expense_id": expense_id,
        "cost": item_json.cost,
        "item_name": item_json.name,
        "user_id": user_id,
    }

