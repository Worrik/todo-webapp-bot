"""added ondelete for tags and performers, and unique tags

Revision ID: 4ef9bbd25400
Revises: 27e04b5b70a3
Create Date: 2022-07-25 20:46:15.205542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ef9bbd25400'
down_revision = '27e04b5b70a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('performers_user_id_fkey', 'performers', type_='foreignkey')
    op.drop_constraint('performers_todo_id_fkey', 'performers', type_='foreignkey')
    op.create_foreign_key(None, 'performers', 'todos', ['todo_id'], ['id'], onupdate='cascade', ondelete='cascade')
    op.create_foreign_key(None, 'performers', 'users', ['user_id'], ['id'], onupdate='cascade', ondelete='cascade')
    op.create_unique_constraint(None, 'tags', ['todo_id', 'name'])
    op.drop_constraint('tags_todo_id_fkey', 'tags', type_='foreignkey')
    op.create_foreign_key(None, 'tags', 'todos', ['todo_id'], ['id'], onupdate='cascade', ondelete='cascade')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags', type_='foreignkey')
    op.create_foreign_key('tags_todo_id_fkey', 'tags', 'todos', ['todo_id'], ['id'], onupdate='CASCADE')
    op.drop_constraint(None, 'tags', type_='unique')
    op.drop_constraint(None, 'performers', type_='foreignkey')
    op.drop_constraint(None, 'performers', type_='foreignkey')
    op.create_foreign_key('performers_todo_id_fkey', 'performers', 'todos', ['todo_id'], ['id'], onupdate='CASCADE')
    op.create_foreign_key('performers_user_id_fkey', 'performers', 'users', ['user_id'], ['id'], onupdate='CASCADE')
    # ### end Alembic commands ###
