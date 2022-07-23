from bot.models.base import Base, TimestampMixin

import sqlalchemy as sa


class User(TimestampMixin, Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    __tablename__ = "users"

    id = sa.Column(sa.BigInteger, primary_key=True)

    is_bot = sa.Column(sa.Boolean)
    first_name = sa.Column(sa.String(100))
    last_name = sa.Column(sa.String(100))
    username = sa.Column(sa.String(100), unique=True)
    language_code = sa.Column(sa.String(2))
