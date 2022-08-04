from sqlalchemy.orm import declarative_base
import sqlalchemy as sa


class BaseModel:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    id = sa.Column(sa.Integer, primary_key=True)


class TimestampMixin(BaseModel):
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now())


Base = declarative_base()
metadata = Base.metadata
