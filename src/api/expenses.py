import datetime

import sqlalchemy
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException

from src import database as db
from src import sql_utils as utils
from src.sql_utils import get_category

router = APIRouter()


@router.get("/users/{user_id}/expenses/{expense_id}", tags=["expenses"])
def get_expense(user_id: int, expense_id: int, password: str):
    """
    This endpoint returns the information associated with an expense by its identifier.
    For each expense it returns:

    - `cost`: the monetary value of the expense, in Dollars
    - `date_time`: the date and time of the expense
    - `expense_id`: the ID of the item associated with the expense
    - `category`: the user defined category of the item
    - `description`: the user defined description of the item
    """
    utils.authenticate(user_id, password)
    with db.engine.connect() as conn:
        expense_data = conn.execute(
            sqlalchemy.text('''
            SELECT expense.expense_id, category.category_name, timestamp,
            COALESCE(SUM(item.cost), 0) AS cost, description
            FROM expense
            INNER JOIN category
            ON expense.category_id = category.category_id
            LEFT JOIN item
            ON expense.expense_id = item.expense_id
            WHERE expense.expense_id = :expense_id
            AND category.user_id = :user_id
            GROUP BY expense.expense_id, category.category_id, timestamp, description;
            '''),
            {"expense_id": expense_id, "user_id": user_id}
        ).fetchone()
        if not expense_data:
            raise HTTPException(status_code=404, detail="expense not found.")
    return {
        "cost": expense_data.cost,
        "date_time": expense_data.timestamp,
        "expense_id": expense_data.expense_id,
        "category": expense_data.category_name,
        "description": expense_data.description,
    }


@router.get("/users/{user_id}/expenses", tags=["expenses"])
def list_expenses(user_id: int,
                  password: str,
                  limit: int = 10,
                  offset: int = 0,
                  start_date: datetime.date =
                  datetime.datetime.utcnow().date() - datetime.timedelta(days=7),
                  end_date: datetime.date = datetime.datetime.utcnow().date(),
                  ):
    """
    This endpoint returns the information associated with expenses
    over a defined time period.
    By default, the difference between `start_date` and `end_date` is one week
    and `end_time` is today.
    Expects format "YYYY-MM-DD HH:MM:SS" for timestamp

    For each expense, it returns:

    - `cost`: the monetary value of the expense, in dollars
    - `date`: the date of the expense
    - `expense_id`: the ID of the item associated with the expense
    - `category`: the user-defined category of the item
    """
    utils.authenticate(user_id, password)
    with db.engine.begin() as conn:
        expenses = conn.execute(
            sqlalchemy.text(
                '''
                SELECT expense.expense_id, category.category_name, timestamp,
                COALESCE(SUM(item.cost), 0) AS cost, description
                FROM expense
                INNER JOIN category
                ON expense.category_id = category.category_id
                LEFT JOIN item
                ON expense.expense_id = item.expense_id
                WHERE category.user_id = :user_id
                AND date(timestamp) BETWEEN :start_date and :end_date
                GROUP BY expense.expense_id, category.category_id,
                timestamp, description
                LIMIT :limit
                OFFSET :offset;
                ''',
            ),
            {
                "user_id": user_id,
                "end_date": end_date,
                "start_date": start_date,
                "limit": limit,
                "offset": offset,
            }
        ).fetchall()
        return [
            {
                "expense_id": expense.expense_id,
                "cost": expense.cost,
                "date_time": expense.timestamp,
                "description": expense.description,
                "category": expense.category_name,
            }
            for expense in expenses
        ]


# Expects format "YYYY-MM-DD HH:MM:SS" for timestamp
class ExpenseJson(BaseModel):
    date_time: datetime.datetime
    category_id: int
    description: str


@router.post("/users/{user_id}/expenses/", tags=["expenses"])
def add_expense(user_id: int, password: str, expense_json: ExpenseJson):
    """
    This endpoint adds a new expense to the database.
    This expense includes:

    - `user`: the user who is adding the expense (required)
    - `cost`: the monetary value of the expense, in Dollars (required)
    - `date_time`: the date and time of the expense. (required)
    - `category_id`: the budget category of the item (required)
    - `description`: the user defined description of the item (not required)
    """
    utils.authenticate(user_id, password)
    get_category(user_id, expense_json.category_id)
    with db.engine.begin() as conn:
        inserted_expense = conn.execute(
            sqlalchemy.text(
                '''
            INSERT into expense (timestamp, category_id, description)
            VALUES (:date_time, :category_id, :description)
            RETURNING expense_id;
            '''
            ),
            {
                "date_time": expense_json.date_time,
                "category_id": expense_json.category_id,
                "description": expense_json.description
            }
        )
    expense = inserted_expense.fetchone()
    return {
        "expense_id": expense.expense_id,
        "category_id": expense_json.category_id,
        "date_time": expense_json.date_time,
        "description": expense_json.description,
    }
