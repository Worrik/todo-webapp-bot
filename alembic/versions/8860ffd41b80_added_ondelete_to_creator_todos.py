"""added ondelete to creator todos

Revision ID: 8860ffd41b80
Revises: 2549d5e84a31
Create Date: 2022-08-12 15:01:55.947436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8860ffd41b80'
down_revision = '2549d5e84a31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('todos_creator_id_fkey', 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'users', ['creator_id'], ['id'], onupdate='cascade', ondelete='cascade')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key('todos_creator_id_fkey', 'todos', 'users', ['creator_id'], ['id'], onupdate='CASCADE')
    # ### end Alembic commands ###
