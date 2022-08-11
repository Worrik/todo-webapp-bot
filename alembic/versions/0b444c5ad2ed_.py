"""empty message

Revision ID: 0b444c5ad2ed
Revises: 2cb58a934315
Create Date: 2022-08-04 19:31:14.600304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0b444c5ad2ed"
down_revision = "2cb58a934315"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("todos_status_id_fkey", "todos", type_="foreignkey")
    op.drop_column("todos", "status_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "todos",
        sa.Column("status_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "todos_status_id_fkey",
        "todos",
        "statuses",
        ["status_id"],
        ["id"],
        ondelete="SET NULL",
    )
    # ### end Alembic commands ###
