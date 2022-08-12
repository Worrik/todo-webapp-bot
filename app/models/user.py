from typing import List, Union
from app.models.base import Base, TimestampMixin
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

import sqlalchemy as sa

if TYPE_CHECKING:
    from .todo import Todo


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Union[sa.Column, int] = sa.Column(sa.BigInteger, primary_key=True)

    is_bot: Union[sa.Column, bool] = sa.Column(sa.Boolean)
    first_name: Union[sa.Column, str] = sa.Column(sa.String(100))
    last_name: Union[sa.Column, str] = sa.Column(sa.String(100))
    username: Union[sa.Column, str] = sa.Column(sa.String(100), unique=True)
    language_code: Union[sa.Column, str] = sa.Column(sa.String(2))

    todos: Union[relationship, List["Todo"]] = relationship(
        "Todo", secondary="performers", back_populates="users"
    )
    created_todos: Union[relationship, List["Todo"]] = relationship(
        "Todo", back_populates="creator"
    )
