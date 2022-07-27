from models.base import Base, TimestampMixin
from sqlalchemy.orm import relationship

import sqlalchemy as sa


class Group(TimestampMixin, Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    __tablename__ = "groups"

    id = sa.Column(sa.BigInteger, primary_key=True)
    type = sa.Column(sa.String(50))
    title = sa.Column(sa.String(50))
    username = sa.Column(sa.String(100))
    description = sa.Column(sa.String(250))
    invite_link = sa.Column(sa.String(250))

    todos = relationship("Todo", back_populates="group")


class GroupUser(Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    __tablename__ = "group_users"

    user_id = sa.Column(
        sa.ForeignKey("users.id", onupdate="cascade"), primary_key=True
    )
    group_id = sa.Column(
        sa.ForeignKey("groups.id", onupdate="cascade"), primary_key=True
    )

    __table_args__ = (sa.UniqueConstraint("user_id", "group_id"),)
