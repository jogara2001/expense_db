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
    This endpoint returns the information associated with all users.
    For each user it returns:

    - `user_id`: the ID of the user
    - `name`: the name of the user

    You can filter for users whose name contain a string by using the
    `name` query parameter.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
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
def get_user(user_id: int):
    """
    This endpoint returns the information associated with a user by its identifier.
    For each user it returns:

    - `user_id`: the ID of the user
    - `name`: the name of the user
    """
    with db.engine.connect() as conn:
        user = conn.execute(
            sqlalchemy.text('SELECT user_id, name FROM "user" '
                            'WHERE user_id = :user_id'),
            {"user_id": user_id}
        ).fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="user not found.")
    return {
        "user_id": user.user_id,
        "name": user.name,
    }


class UserJson(BaseModel):
    name: str
    password: str


@router.post("/users/", tags=["users"])
def create_user(user: UserJson):
    """
    This endpoint creates a new user.

    Takes in a UserJson which contains the user's name.

    Returns the user's ID and name if successful.
    """
    if not username_unique(user.name):
        raise HTTPException(status_code=404, detail="name already taken")

    with db.engine.connect() as conn:
        with conn.begin():
            inserted_user = conn.execute(
                sqlalchemy.text(
                'INSERT INTO "user" (name, hashed_pwd) VALUES '
                '(:name, extensions.crypt(:password, extensions.gen_salt(\'bf\'))) '
                'RETURNING user_id'
                ),
                [{"name": user.name,
                 "password": user.password}]
            )
            user_id = inserted_user.fetchone().user_id
    return {
        "user_id": user_id,
        "name": user.name,
    }
