import sqlalchemy
from fastapi import HTTPException
from src import database as db


def get_user(user_id: int):
    with db.engine.connect() as conn:
        user = conn.execute(
            sqlalchemy.text('SELECT * FROM "user" WHERE user_id = :user_id'),
            [{"user_id": user_id}]
        ).fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="user not found.")
    return user


def get_expense(expense_id: int):
    with db.engine.connect() as conn:
        expense = conn.execute(
            sqlalchemy.text(
                "SELECT * FROM expense WHERE expense_id = :expense_id"),
            [{"expense_id": expense_id}]
        ).fetchone()
        if expense is None:
            raise HTTPException(status_code=404, detail="expense not found.")
    return expense


def get_category(user_id: int, budget_category_id: int):
    with db.engine.connect() as conn:
        category_user = conn.execute(
            sqlalchemy.text('''
            SELECT * FROM category
            WHERE user_id = :user_id
            AND category_id = :category_id
            '''),
            [{"user_id": user_id, "category_id": budget_category_id}]
        ).fetchone()
        if category_user is None:
            raise HTTPException(
                status_code=404, detail="category not found.")
    return category_user
