"""empty message

Revision ID: 8154c867827f
Revises: 5d7a2cdaae8b
Create Date: 2022-07-21 18:56:25.211789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8154c867827f"
down_revision = "5d7a2cdaae8b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "groups",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=True),
        sa.Column("title", sa.String(length=50), nullable=True),
        sa.Column("username", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=250), nullable=True),
        sa.Column("invite_link", sa.String(length=250), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("groups")
    # ### end Alembic commands ###
