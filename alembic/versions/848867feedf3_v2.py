from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision = '848867feedf3'
down_revision = '257db456f6bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    op.create_table(
        "user",
        sa.Column("user_id", sa.BIGINT, autoincrement=True, primary_key=True),
        sa.Column("name", sa.TEXT, nullable=False),
        sa.Column("hashed_pwd", sa.TEXT, nullable=False)
    )
    op.create_table(
        "category",
        sa.Column("category_id", sa.BIGINT,
                  autoincrement=True, primary_key=True),
        sa.Column(
            "user_id",
            sa.BIGINT,
            ForeignKey("user.user_id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("category_name", sa.TEXT, nullable=False)
    )
    op.create_table(
        "budget",
        sa.Column("budget_id", sa.BIGINT,
                  autoincrement=True, primary_key=True),
        sa.Column(
            "category_id",
            sa.BIGINT,
            ForeignKey("category.category_id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("start_date", sa.TIMESTAMP, nullable=False),
        sa.Column("end_date", sa.TIMESTAMP, nullable=False),
        sa.Column("budget", sa.DECIMAL, nullable=False)
    )
    op.create_table(
        "expense",
        sa.Column("expense_id", sa.BIGINT,
                  autoincrement=True, primary_key=True),
        sa.Column(
            "category_id",
            sa.BIGINT,
            ForeignKey("category.category_id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("timestamp", sa.TIMESTAMP, nullable=False),
        sa.Column("description", sa.TEXT, nullable=False)
    )
    op.create_table(
        "item",
        sa.Column("item_id", sa.BIGINT, autoincrement=True, primary_key=True),
        sa.Column(
            "expense_id",
            sa.BIGINT,
            ForeignKey("expense.expense_id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("cost", sa.DECIMAL, nullable=False),
        sa.Column("name", sa.TEXT, nullable=False)
    )
    op.create_table(
        "deposit",
        sa.Column("deposit_id", sa.BIGINT,
                  autoincrement=True, primary_key=True),
        sa.Column(
            "user_id",
            sa.BIGINT,
            ForeignKey("user.user_id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("amount", sa.DECIMAL, nullable=False),
        sa.Column("timestamp", sa.TIMESTAMP, nullable=False),
    )


def downgrade() -> None:
    pass
