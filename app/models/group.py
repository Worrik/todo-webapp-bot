from typing import List, Union
from app.models.base import Base, TimestampMixin
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

import sqlalchemy as sa

if TYPE_CHECKING:
    from .todo import Todo


class Group(TimestampMixin, Base):
    __tablename__ = "groups"

    id: Union[sa.Column, int] = sa.Column(sa.BigInteger, primary_key=True)
    type: Union[sa.Column, str] = sa.Column(sa.String(50))
    title: Union[sa.Column, str] = sa.Column(sa.String(50))
    username: Union[sa.Column, str] = sa.Column(sa.String(100))
    description: Union[sa.Column, str] = sa.Column(sa.String(250))
    invite_link: Union[sa.Column, str] = sa.Column(sa.String(250))
    photo: Union[sa.Column, str] = sa.Column(sa.String(500))

    todos: Union[relationship, List["Todo"]] = relationship(
        "Todo", back_populates="group"
    )


class GroupUser(Base):
    __tablename__ = "group_users"

    user_id: Union[sa.Column, int] = sa.Column(
        sa.ForeignKey("users.id", onupdate="cascade", ondelete="cascade"),
        primary_key=True,
    )
    group_id: Union[sa.Column, int] = sa.Column(
        sa.ForeignKey("groups.id", onupdate="cascade", ondelete="cascade"),
        primary_key=True,
    )

    __table_args__ = (sa.UniqueConstraint("user_id", "group_id"),)
