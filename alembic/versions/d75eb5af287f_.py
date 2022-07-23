"""empty message

Revision ID: d75eb5af287f
Revises: 70a6b1611ffd
Create Date: 2022-07-23 00:51:00.201833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d75eb5af287f"
down_revision = "70a6b1611ffd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "performers_user_id_fkey", "performers", type_="foreignkey"
    )
    op.create_foreign_key(None, "performers", "users", ["user_id"], ["id"])
    op.add_column(
        "todos", sa.Column("group_id", sa.BigInteger(), nullable=True)
    )
    op.drop_constraint("todos_creator_id_fkey", "todos", type_="foreignkey")
    op.create_foreign_key(None, "todos", "users", ["creator_id"], ["id"])
    op.create_foreign_key(None, "todos", "groups", ["group_id"], ["id"])
    op.drop_table("group_users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "todos", type_="foreignkey")
    op.drop_constraint(None, "todos", type_="foreignkey")
    op.create_foreign_key(
        "todos_creator_id_fkey", "todos", "group_users", ["creator_id"], ["id"]
    )
    op.drop_column("todos", "group_id")
    op.drop_constraint(None, "performers", type_="foreignkey")
    op.create_foreign_key(
        "performers_user_id_fkey",
        "performers",
        "group_users",
        ["user_id"],
        ["id"],
    )
    op.create_table(
        "group_users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column("group_id", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["group_id"], ["groups.id"], name="group_users_group_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="group_users_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="group_users_pkey"),
        sa.UniqueConstraint(
            "user_id", "group_id", name="group_users_user_id_group_id_key"
        ),
    )
    # ### end Alembic commands ###