"""empty message

Revision ID: 26996624fe81
Revises: 20cc512afd7e
Create Date: 2022-07-23 17:08:23.628682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "26996624fe81"
down_revision = "20cc512afd7e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tags", sa.Column("name", sa.String(length=50), nullable=True)
    )
    op.drop_column("tags", "name_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tags",
        sa.Column(
            "name_id",
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("tags", "name")
    # ### end Alembic commands ###