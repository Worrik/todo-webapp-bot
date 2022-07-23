from bot.models.base import Base, TimestampMixin
from sqlalchemy.orm import relationship

import sqlalchemy as sa


class Todo(TimestampMixin, Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    __tablename__ = "todos"

    creator_id = sa.Column(sa.ForeignKey("users.id", onupdate="cascade"))
    creator = relationship("User", back_populates="created_todos")

    group_id = sa.Column(sa.ForeignKey("groups.id", onupdate="cascade"))
    group = relationship("Group", back_populates="todos")

    users = relationship(
        "User", secondary="performers", back_populates="todos", lazy=False
    )
    tags = relationship("Tag", back_populates="todo", lazy=False)

    text = sa.Column(sa.Text)
    message_id = sa.Column(sa.BigInteger, nullable=False)


class Performer(TimestampMixin, Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    __tablename__ = "performers"

    todo_id = sa.Column(sa.ForeignKey("todos.id", onupdate="cascade"))
    user_id = sa.Column(sa.ForeignKey("users.id", onupdate="cascade"))


class Tag(TimestampMixin, Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    __tablename__ = "tags"

    todo_id = sa.Column(sa.ForeignKey("todos.id", onupdate="cascade"))
    todo = relationship("Todo", back_populates="tags")
    name = sa.Column(sa.String(50))
