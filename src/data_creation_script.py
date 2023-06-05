import datetime

from src import database as db
import sqlalchemy
from sqlalchemy.orm import Session


def generate_data(num: int):
    with db.engine.connect() as conn:
        user_obj = db.user.insert()
        conn.execute(
            user_obj,
            [{
                "user_id": i,
                "name": f"user{i}",
                "hashed_pwd": "password"
            } for i in range(num)]
        )
        print("finished users")

        deposit_obj = db.deposit.insert()
        conn.execute(
            deposit_obj,
            [{
                "deposit_id": i,
                "user_id": i,
                "amount": 100,
                "timestamp": datetime.datetime.utcnow()
            } for i in range(num)]
        )
        print("finished deposits")

        category_obj = db.category.insert()
        conn.execute(
            category_obj,
            [{
                "category_id": i,
                "user_id": i,
                "category_name": "category",
            } for i in range(num)]
        )
        print("finished categories")

        budget_obj = db.budget.insert()
        conn.execute(
            budget_obj,
            [{
                "budget_id": i,
                "category_id": i,
                "start_date": datetime.datetime.utcnow(),
                "end_date": datetime.datetime.utcnow(),
                "budget": 100
            } for i in range(num)]
        )
        print("finished budgets")

        expense_obj = db.expense.insert()
        conn.execute(
            expense_obj,
            [{
                "expense_id": i,
                "category_id": i,
                "timestamp": datetime.datetime.utcnow(),
                "description": "test data"
            } for i in range(num)]
        )
        print("finished expenses")

        item_obj = db.item.insert()
        conn.execute(
            item_obj,
            [{
                "item_id": i,
                "expense_id": i,
                "cost": 10,
                "name": "test data"
            } for i in range(num)]
        )
        print("finished items")
        conn.commit()


if __name__ == "__main__":
    generate_data(1000000)
