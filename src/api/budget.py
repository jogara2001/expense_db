import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import datetime

from src import database as db

router = APIRouter()


class BudgetJson(BaseModel):
    budget: float
    start_date: datetime.date = datetime.datetime.utcnow().date()
    end_date: datetime.date = datetime.datetime.utcnow().date() + \
        datetime.timedelta(days=7)


@router.post("/users/{user_id}/categories/{category_id}/budget/", tags=["budgets"])
def add_budget(
    category_id: int,
    budget_entry: BudgetJson
):
    """
    This endpoint adds or updates a category with a budget. It takes as input:

    - `user_id`: the associated user for the budget
    - `budget_category`: the user generated category to be created/updated
    - `budget`: the dollar amount of the budget
    """
    with db.engine.begin() as conn:
        budget = conn.execute(sqlalchemy.text('''
            INSERT INTO budget (category_id, start_date, end_date, budget)
            VALUES (:category_id, :start, :end, :amount)
            RETURNING budget_id, category_id, start_date, end_date, budget
        '''), {
            "category_id": category_id,
            "start": budget_entry.start_date,
            "end": budget_entry.end_date,
            "amount": budget_entry.budget
        }).fetchone()
    return {
        "budget_id": budget.budget_id,
        "category_id": budget.category_id,
        "start_date": budget.start_date,
        "end_date": budget.end_date,
        "budget": budget.budget
    }


@router.get(
    "/users/{user_id}/categories/{category_id}/budget/{budget_id}/",
    tags=["budgets"]
)
def get_budget(user_id: int, category_id: int, budget_id: int):
    """
    This endpoint returns a budget entry for a given budget_id
    """
    with db.engine.connect() as conn:
        # Check for category id as well
        budget = conn.execute(sqlalchemy.text(
            '''
            SELECT budget_id, budget.category_id,
            start_date, end_date, budget
            FROM budget
            JOIN category ON budget.category_id = category.category_id
            JOIN "user" ON category.user_id = "user".user_id
            WHERE budget_id = :budget_id
            AND "user".user_id = :user_id
            AND budget.category_id = :category_id;
            '''
        ), {
            "budget_id": budget_id,
            "user_id": user_id,
            "category_id": category_id
        }).fetchone()
        if budget is None:
            raise HTTPException(status_code=404, detail="budget not found.")
    return {
        "budget_id": budget.budget_id,
        "category_id": budget.category_id,
        "start_date": budget.start_date,
        "end_date": budget.end_date,
        "budget": budget.budget
    }


@router.get(
    "/users/{user_id}/categories/{category_id}/budget/",
    tags=["budgets"]
)
def list_budget(user_id: int, limit: int = 10, offset: int = 0):
    """
    This endpoint returns all the budget information associated with a user
    For each budget, the following is returned:
    `budget_id`: the id of the budget
    `category_name`: the category the budget is associated with
    `start_date`: the designated start date of the budget
    `end_date`: the designated end date of the budget
    `amount`: the amount allocated for the budget
    """
    data = []
    with db.engine.connect() as conn:
        budgets = conn.execute(sqlalchemy.text(
            '''
            SELECT b.budget_id, c.category_name,
            b.start_date, b.end_date, b.budget amount FROM budget AS b
            JOIN category AS c ON c.category_id = b.category_id
            WHERE c.user_id = :user_id
            LIMIT :limit
            OFFSET :offset;
            '''
        ), {"user_id": user_id, "limit": limit, "offset": offset}).fetchall()
    for budget in budgets:
        data.append({
            "budget_id": budget.budget_id,
            "category_name": budget.category_name,
            "start_date": budget.start_date,
            "end_date": budget.end_date,
            "amount_allocated": budget.amount
        })
    return data
