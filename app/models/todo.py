from datetime import datetime
from typing import List, Union
from app.models.base import Base, TimestampMixin
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

import sqlalchemy as sa

if TYPE_CHECKING:
    from .user import User
    from .group import Group


class Todo(TimestampMixin, Base):
    __tablename__ = "todos"

    id: Union[sa.Column, int] = sa.Column(
        sa.BigInteger, nullable=False, primary_key=True
    )

    creator_id: Union[sa.Column, int] = sa.Column(
        sa.ForeignKey("users.id", onupdate="cascade", ondelete="cascade")
    )
    creator: Union[relationship, "User"] = relationship(
        "User", back_populates="created_todos", lazy=False
    )

    group_id: Union[sa.Column, int] = sa.Column(
        sa.ForeignKey("groups.id", onupdate="cascade"), primary_key=True
    )
    group: Union[relationship, "Group"] = relationship(
        "Group", back_populates="todos"
    )

    users: Union[relationship, "User"] = relationship(
        "User", secondary="performers", back_populates="todos", lazy=False
    )
    tags: Union[relationship, "Tag"] = relationship(
        "Tag", back_populates="todo", lazy=False
    )

    status_name: Union[sa.Column, str] = sa.Column(
        sa.ForeignKey("statuses.name", ondelete="set null")
    )
    status: Union[relationship, "Status"] = relationship(
        "Status", back_populates="todos", lazy=False
    )

    text: Union[sa.Column, str] = sa.Column(sa.Text)

    additional_info_id: Union[sa.Column, int] = sa.Column(
        sa.ForeignKey("additional_info.id", ondelete="set null")
    )
    additional_info: Union[relationship, "AdditionalInfo"] = relationship(
        "AdditionalInfo", back_populates="todo", lazy=False
    )

    deadline: Union[sa.Column, datetime] = sa.Column(sa.DateTime)

    __table_args__ = (sa.UniqueConstraint("id", "group_id"),)


class Status(Base):
    __tablename__ = "statuses"

    name: Union[sa.Column, str] = sa.Column(
        sa.String(100), primary_key=True, unique=True, nullable=False
    )
    todos: Union[relationship, List[Todo]] = relationship(
        "Todo", back_populates="status"
    )


class Performer(TimestampMixin, Base):
    __tablename__ = "performers"

    todo_id: Union[sa.Column, int] = sa.Column(sa.BigInteger)
    todo_group_id: Union[sa.Column, int] = sa.Column(sa.BigInteger)
    user_id: Union[sa.Column, int] = sa.Column(
        sa.ForeignKey("users.id", onupdate="cascade", ondelete="cascade")
    )
    __table_args__ = (
        sa.UniqueConstraint("todo_id", "todo_group_id", "user_id"),
        sa.ForeignKeyConstraint(
            ["todo_id", "todo_group_id"],
            ["todos.id", "todos.group_id"],
            onupdate="cascade",
            ondelete="cascade",
        ),
    )


class Tag(TimestampMixin, Base):
    __tablename__ = "tags"

    todo_id: Union[sa.Column, int] = sa.Column(sa.BigInteger)
    todo_group_id: Union[sa.Column, int] = sa.Column(sa.BigInteger)
    todo: Union[relationship, Todo] = relationship(
        "Todo", back_populates="tags"
    )
    name: Union[sa.Column, str] = sa.Column(sa.String(50))

    __table_args__ = (
        sa.UniqueConstraint("todo_id", "name"),
        sa.ForeignKeyConstraint(
            ["todo_id", "todo_group_id"], ["todos.id", "todos.group_id"]
        ),
    )


class AdditionalInfo(TimestampMixin, Base):
    __tablename__ = "additional_info"

    id: Union[sa.Column, int] = sa.Column(
        sa.BigInteger, nullable=False, primary_key=True
    )

    todos: Union[relationship, Todo] = relationship(
        "Todo", back_populates="additional_info", uselist=False
    )

    text: Union[sa.Column, str] = sa.Column(sa.Text)
