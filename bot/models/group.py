from bot.models.base import Base, TimestampMixin

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
