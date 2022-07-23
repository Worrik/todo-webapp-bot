from bot.models.base import Base, TimestampMixin

import sqlalchemy as sa


class Todo(TimestampMixin, Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    __tablename__ = "todos"

    creator_id = sa.Column(sa.ForeignKey("users.id", onupdate="cascade"))
    group_id = sa.Column(sa.ForeignKey("groups.id", onupdate="cascade"))
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
    name_id = sa.Column(sa.String(50))
