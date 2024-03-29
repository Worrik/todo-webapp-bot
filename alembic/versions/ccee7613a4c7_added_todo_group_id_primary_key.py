"""added todo.group_id primary key

Revision ID: ccee7613a4c7
Revises: 88e2400e7c9a
Create Date: 2022-08-02 17:25:45.256776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ccee7613a4c7"
down_revision = "88e2400e7c9a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "todos", "group_id", existing_type=sa.BIGINT(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "todos", "group_id", existing_type=sa.BIGINT(), nullable=True
    )
    # ### end Alembic commands ###
