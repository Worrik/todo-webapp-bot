"""empty message

Revision ID: 5d7a2cdaae8b
Revises: 750633fade02
Create Date: 2022-07-21 17:07:20.873401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5d7a2cdaae8b"
down_revision = "750633fade02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "telegram_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "telegram_id", sa.BIGINT(), autoincrement=False, nullable=False
        ),
    )
    # ### end Alembic commands ###