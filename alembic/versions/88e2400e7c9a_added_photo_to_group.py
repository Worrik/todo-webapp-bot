"""added photo to group

Revision ID: 88e2400e7c9a
Revises: 6e97bda2d2f1
Create Date: 2022-08-02 17:07:15.002189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "88e2400e7c9a"
down_revision = "6e97bda2d2f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("groups", sa.Column("photo", sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("groups", "photo")
    # ### end Alembic commands ###
