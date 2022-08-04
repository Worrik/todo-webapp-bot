"""empty message

Revision ID: 25557219a968
Revises: 0b444c5ad2ed
Create Date: 2022-08-04 19:33:02.640969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25557219a968'
down_revision = '0b444c5ad2ed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'statuses', ['name'])
    op.drop_column('statuses', 'id')
    op.add_column('todos', sa.Column('status_name', sa.String(length=100), nullable=True))
    op.create_foreign_key(None, 'todos', 'statuses', ['status_name'], ['name'], ondelete='set null')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'status_name')
    op.add_column('statuses', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'statuses', type_='unique')
    # ### end Alembic commands ###
