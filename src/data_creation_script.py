import datetime
import os
from faker import Faker
import dotenv
import sqlalchemy


dotenv.load_dotenv()
DB_USER: str = os.environ.get("POSTGRES_USER")
DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
DB_PORT: str = os.environ.get("POSTGRES_PORT")
DB_NAME: str = os.environ.get("POSTGRES_DB")

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}")

metadata_obj = sqlalchemy.MetaData()
user = sqlalchemy.Table("user", metadata_obj, autoload_with=engine)
deposit = sqlalchemy.Table("deposit", metadata_obj, autoload_with=engine)
expense = sqlalchemy.Table("expense", metadata_obj, autoload_with=engine)
category = sqlalchemy.Table("category", metadata_obj, autoload_with=engine)
budget = sqlalchemy.Table("budget", metadata_obj, autoload_with=engine)
item = sqlalchemy.Table("item", metadata_obj, autoload_with=engine)


def generate_data(num: int):
    fake = Faker()
    with engine.connect() as conn:
        user_obj = user.insert()
        conn.execute(
            user_obj,
            [{
                "user_id": i,
                "name": fake.unique.email(),
                "hashed_pwd": "password"
            } for i in range(num)]
        )
        print("finished users")

        deposit_obj = deposit.insert()
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

        category_obj = category.insert()
        conn.execute(
            category_obj,
            [{
                "category_id": i,
                "user_id": i,
                "category_name": fake.sentence(),
            } for i in range(num)]
        )
        print("finished categories")

        budget_obj = budget.insert()
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

        expense_obj = expense.insert()
        conn.execute(
            expense_obj,
            [{
                "expense_id": i,
                "category_id": i,
                "timestamp": datetime.datetime.utcnow(),
                "description": fake.sentence()
            } for i in range(num)]
        )
        print("finished expenses")

        item_obj = item.insert()
        conn.execute(
            item_obj,
            [{
                "item_id": i,
                "expense_id": i,
                "cost": 10,
                "name": fake.sentence()
            } for i in range(num)]
        )
        print("finished items")
        conn.commit()


if __name__ == "__main__":
    generate_data(100)
