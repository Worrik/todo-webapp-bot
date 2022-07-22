from sqlalchemy.orm import declarative_base
import sqlalchemy as sa


class BaseModel:
    id = sa.Column(sa.Integer, primary_key=True)


class TimestampMixin:
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())


Base = declarative_base(cls=BaseModel)
metadata = Base.metadata
