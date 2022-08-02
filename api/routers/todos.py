from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

import sqlalchemy as sa

from db import get_session
from ...models import Todo, Performer
from ...models.pydantic_models import TodoPydantic


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
