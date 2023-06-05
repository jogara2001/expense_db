import sqlalchemy
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src import database as db
from src.sql_utils import username_unique

router = APIRouter()


@router.get("/users/", tags=["users"])
def list_users(
        name: str = "",
        limit: int = Query(50, ge=1, le=250),
        offset: int = Query(0, ge=0),
):
    """
    This lists the users (primarily used for debugging purposes)

    - `name`: filter for name of user
    - `limit`: the maximum number of results to return
    - `offset`: the number of results to skip
    - `return`: a list of users
    """

    with db.engine.connect() as conn:
        query = 'SELECT user_id, name FROM "user"'
        parameters = {
            "limit": limit,
            "offset": offset
        }
        if name != "":
            query += 'WHERE name like :name '
            parameters["name"] = name

        query += 'LIMIT :limit ' \
                 'OFFSET :offset'

        users = conn.execute(
            sqlalchemy.text(query),
            parameters
        ).fetchall()
    return [
        {
            "user_id": user.user_id,
            "name": user.name,
        }
        for user in users
    ]


@router.get("/users/{user_id}/", tags=["users"])
def get_user(
        user_id: int,
):
    """
    This endpoint returns the information associated with a user by its identifier.

    - `user_id`: the ID of the user
    - `return`: the specified user
        - `user_id`: the ID of the user
        - `name`: the name of the user
        - `balance`: the total balance of their account
    """

    with db.engine.connect() as conn:
        user = conn.execute(
            sqlalchemy.text('''
            select deposits.user_id, deposits.name, deposits_sum - costs_sum as balance
            from
            
            (select "user".user_id, "user".name, 
            COALESCE(sum(deposit.amount), 0) as deposits_sum
            from "user"
            left JOIN deposit on deposit.user_id = "user".user_id
            WHERE "user".user_id = :user_id
            GROUP BY "user".user_id, "user".name) deposits
            
            join
            
            (select "user".user_id, "user".name,
            COALESCE(sum(item.cost), 0) as costs_sum
            from "user"
            left JOIN category ON category.user_id = "user".user_id
            left JOIN expense ON expense.category_id = category.category_id
            left JOIN item on item.expense_id = expense.expense_id
            WHERE "user".user_id = :user_id
            GROUP BY "user".user_id, "user".name) costs
            
            on deposits.user_id = costs.user_id
            '''),
            {"user_id": user_id}
        ).fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="user not found.")
    return {
        "user_id": user.user_id,
        "name": user.name,
        "balance": user.balance
    }


class UserJson(BaseModel):
    name: str
    password: str


@router.post("/users/", tags=["users"])
def create_user(user: UserJson):
    """
    This endpoint creates a new user.

    - `user`: an object consisting of the following
        - `name`: the name of the user (must be unique)
        - `password`: the password for the user
    - `return`: the resulting user entry
    """
    if not username_unique(user.name):
        raise HTTPException(status_code=404, detail="name already taken")

    with db.engine.connect() as conn:
        with conn.begin():
            inserted_user = conn.execute(
                sqlalchemy.text('''
                    INSERT INTO "user" (name, hashed_pwd) VALUES
                    (:name, extensions.crypt(:password, extensions.gen_salt(\'bf\')))
                    RETURNING user_id
                '''),
                {
                    "name": user.name,
                    "password": user.password
                }
            )
            user_id = inserted_user.fetchone().user_id
    return {
        "user_id": user_id,
        "name": user.name,
    }


@router.post("/users/login", tags=["users"])
def login_user(username: str, password: str):
    with db.engine.connect() as conn:
        users = conn.execute(
            sqlalchemy.text('''
            SELECT user_id from "user"
            WHERE name = :user_name
            AND hashed_pwd = extensions.crypt(:password, hashed_pwd)
            '''),
            {
                "user_name": username,
                "password": password
            }
        ).fetchall()
        if len(users) != 1:
            raise HTTPException(status_code=401, detail="username or password incorrect")

    return {
        "message": "Signed in"
    }
