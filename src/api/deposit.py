import datetime

import sqlalchemy
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import DateTime

from src import database as db
from src.sql_utils import authenticate

router = APIRouter()


@router.get("/user/{user_id}/deposits/", tags=["deposits"])
def list_deposits(
        user_id: int,
        password: str,
        start_date: datetime.date = datetime.datetime.utcnow().date() - datetime.timedelta(days=7),
        end_date: datetime.date = datetime.datetime.utcnow().date(),
        limit: int = Query(50, ge=1, le=250),
        offset: int = Query(0, ge=0)
):
    authenticate(user_id, password)

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
        password: str,
        deposit: DepositJson,
):
    authenticate(user_id, password)

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
