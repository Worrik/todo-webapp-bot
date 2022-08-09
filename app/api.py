from typing import List
from fastapi import FastAPI
from fastapi.params import Depends, Header
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from aiogram.utils.web_app import safe_parse_webapp_init_data

from app.models import (
    Todo,
    Status,
    Group,
    User,
    GroupUser,
    GroupPydantic,
    StatusPydantic,
    TodoPydantic,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL, TOKEN

import sqlalchemy as sa

from app.models.todo import Performer


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/web", StaticFiles(directory="web", html=True), name="web")


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session():
    async with async_session() as session:
        yield session


async def get_telegram_user(
    session: AsyncSession = Depends(get_session),
    Authorization: str = Header(default=""),
) -> User:
    try:
        data = safe_parse_webapp_init_data(
            token=TOKEN, init_data=Authorization
        )
    except ValueError:
        raise HTTPException(400)

    if not data.user:
        raise HTTPException(400)

    user = await session.get(User, data.user.id)
    return user


@app.get("/groups")
async def get_groups(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_telegram_user),
) -> List[GroupPydantic]:
    q = sa.select(
        [
            Group.id,
            Group.type,
            Group.title,
            Group.username,
            Group.description,
            Group.photo,
            sa.func.count(Todo.id).label("todos_count"),
        ],
    )
    q = q.where(GroupUser.user_id == user.id)
    q = q.group_by(Group.id)
    q = q.outerjoin(Todo, Todo.group_id == Group.id)
    q = q.join(GroupUser, GroupUser.group_id == Group.id)

    res = await session.execute(q)
    groups = res.all()
    return [GroupPydantic.from_orm(group) for group in groups]


@app.get("/groups/{group_id}/todos")
async def todos(
    group_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_telegram_user),
) -> List[TodoPydantic]:
    q = sa.select(Todo).order_by(Todo.created_at.desc())
    q = q.where(Group.id == group_id)
    q = q.where(
        sa.and_(GroupUser.user_id == user.id, GroupUser.group_id == group_id)
    )
    q = q.join(Group, Group.id == Todo.group_id)
    q = q.outerjoin(
        Performer,
        Performer.todo_id == Todo.id
        and Performer.todo_group_id == Todo.group_id,
    )
    q = q.join(GroupUser, GroupUser.user_id == Performer.user_id)

    res = await session.execute(q)
    todos = res.unique().scalars()
    return [TodoPydantic.from_orm(todo) for todo in todos]


@app.put("/groups/{group_id}/todos/{todo_id}/status", status_code=204)
async def set_todo_status(
    group_id: int,
    todo_id: int,
    status: StatusPydantic,
    session: AsyncSession = Depends(get_session),
):
    todo = await session.get(Todo, (todo_id, group_id))

    if not todo or not status.name:
        raise HTTPException(404)

    todo.status = await session.get(Status, status.name)
    session.add(todo)
    await session.commit()


@app.delete("/groups/{group_id}/todos/{todo_id}", status_code=204)
async def delete_todo(
    group_id: int,
    todo_id: int,
    session: AsyncSession = Depends(get_session),
):
    todo = await session.get(Todo, (todo_id, group_id))

    if not todo:
        raise HTTPException(404)

    await session.delete(todo)
    await session.commit()
