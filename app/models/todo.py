from app.models.base import Base, TimestampMixin
from sqlalchemy.orm import relationship

import sqlalchemy as sa


class Todo(TimestampMixin, Base):
    __tablename__ = "todos"

    id = sa.Column(sa.BigInteger, nullable=False, primary_key=True)

    creator_id = sa.Column(sa.ForeignKey("users.id", onupdate="cascade"))
    creator = relationship("User", back_populates="created_todos", lazy=False)

    group_id = sa.Column(
        sa.ForeignKey("groups.id", onupdate="cascade"), primary_key=True
    )
    group = relationship("Group", back_populates="todos")

    users = relationship(
        "User", secondary="performers", back_populates="todos", lazy=False
    )
    tags = relationship("Tag", back_populates="todo", lazy=False)

    status_name = sa.Column(
        sa.ForeignKey("statuses.name", ondelete="set null")
    )
    status = relationship("Status", back_populates="todos", lazy=False)

    text = sa.Column(sa.Text)


class Status(Base):
    __tablename__ = "statuses"

    name = sa.Column(
        sa.String(100), primary_key=True, unique=True, nullable=False
    )
    todos = relationship("Todo", back_populates="status")


class Performer(TimestampMixin, Base):
    __tablename__ = "performers"

    todo_id = sa.Column(sa.BigInteger)
    todo_group_id = sa.Column(sa.BigInteger)
    user_id = sa.Column(
        sa.ForeignKey("users.id", onupdate="cascade", ondelete="cascade")
    )
    __table_args__ = (
        sa.UniqueConstraint("todo_id", "user_id"),
        sa.ForeignKeyConstraint(
            ["todo_id", "todo_group_id"], ["todos.id", "todos.group_id"]
        ),
    )


class Tag(TimestampMixin, Base):
    __tablename__ = "tags"

    todo_id = sa.Column(sa.BigInteger)
    todo_group_id = sa.Column(sa.BigInteger)
    todo = relationship("Todo", back_populates="tags")
    name = sa.Column(sa.String(50))

    __table_args__ = (
        sa.UniqueConstraint("todo_id", "name"),
        sa.ForeignKeyConstraint(
            ["todo_id", "todo_group_id"], ["todos.id", "todos.group_id"]
        ),
    )
