from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.db import get_session
from models import Todo
from models.pydantic_models import TodoPydantic
from models.todo import Performer

import sqlalchemy as sa


router = APIRouter(prefix="/todos")


@router.get("/")
async def todos(user_id: int, session: AsyncSession = Depends(get_session)):
    q = (
        sa.select(Todo)
        .where(Performer.user_id == user_id)
        .join(Performer, Performer.todo_id == Todo.id)
    )
    res = await session.execute(q)
    todos = res.unique().scalars()
    return [TodoPydantic.from_orm(todo) for todo in todos]
