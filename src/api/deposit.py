import datetime

import sqlalchemy
from fastapi import APIRouter, Query
from pydantic import BaseModel

from src import database as db

router = APIRouter()


@router.get("/user/{user_id}/deposits/", tags=["deposits"])
def list_deposits(
        user_id: int,
        start_date: datetime.date =
        datetime.datetime.utcnow().date() - datetime.timedelta(days=7),
        end_date: datetime.date = datetime.datetime.utcnow().date(),
        limit: int = Query(50, ge=1, le=250),
        offset: int = Query(0, ge=0)
):
    """
    This endpoint lists the deposits for a user

    - `user_id`: the user to query
    - `password`: the password for the user
    - `start_date`: the start date for the query (optional
    - `end_date`: the end date for the query (optional)
    - `limit`: the maximum number of results to return
    - `offset`: the number of results to skip
    `return`: a list of deposits

    Each deposit is represented by
    - `deposit_id`: the deposit
    - `amount`: the amount of the deposit
    - `timestamp`: the timestamp of the deposit
    """

    with db.engine.connect() as conn:
        deposits = conn.execute(
            sqlalchemy.text('''
            SELECT deposit_id, amount, timestamp FROM deposit
            WHERE user_id = :user_id
            AND date(timestamp) BETWEEN :start_date and :end_date
            LIMIT :limit
            OFFSET :offset
            '''),
            {
                "user_id": user_id,
                "limit": limit,
                "offset": offset,
                "start_date": start_date,
                "end_date": end_date
            }
        )
        return [
            {
                "deposit_id": deposit.deposit_id,
                "amount": deposit.amount,
                "timestamp": deposit.timestamp
            }
            for deposit in deposits
        ]


class DepositJson(BaseModel):
    amount: float
    timestamp: datetime.datetime


@router.post("/user/{user_id}/deposits/", tags=["deposits"])
def add_deposit(
        user_id: int,
        deposit: DepositJson,
):
    """
    This endpoint adds a deposit to the user specified

    - `user_id`: the user to add the deposit to
    - `deposit`: an object consisting of the following
        - `amount`: the amount of the deposit
        - `timestamp`: the timestamp of the deposit
    return`: the resulting deposit entry
    """

    with db.engine.connect() as conn:
        with conn.begin():
            inserted_deposit = conn.execute(
                sqlalchemy.text('''
                INSERT INTO deposit (user_id, amount, timestamp) VALUES
                (:user_id, :amount, :timestamp) RETURNING deposit_id
                '''),
                {
                    "user_id": user_id,
                    "amount": deposit.amount,
                    "timestamp": deposit.timestamp
                }
            ).fetchone()

            return {
                "deposit_id": inserted_deposit.deposit_id,
                "user_id": user_id,
                "amount": deposit.amount,
                "timestamp": deposit.timestamp
            }
