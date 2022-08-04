from typing import List, Optional
from fastapi import FastAPI
from fastapi.params import Depends, Header
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from aiogram.utils.web_app import safe_parse_webapp_init_data

from models import Todo, Performer, Group, User, GroupUser
from models.pydantic_models import GroupPydantic, TodoPydantic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, TOKEN

import sqlalchemy as sa


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get("/todos")
async def todos(
    group_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_telegram_user),
) -> List[TodoPydantic]:
    q = (
        sa.select(Todo)
        .where(
            sa.or_(Performer.user_id == user.id, Todo.creator_id == user.id)
        )
        .order_by(Todo.created_at.desc())
    )

    if group_id:
        q = q.where(Group.id == group_id)

    q = q.join(Performer, Performer.todo_id == Todo.id)

    res = await session.execute(q)
    todos = res.unique().scalars()
    return [TodoPydantic.from_orm(todo) for todo in todos]


@app.get("/groups")
async def get_groups(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_telegram_user),
) -> List[GroupPydantic]:
    q = (
        sa.select(
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
        .where(GroupUser.user_id == user.id)
        .group_by(Group.id)
        .outerjoin(Todo, Todo.group_id == Group.id)
        .join(GroupUser, GroupUser.group_id == Group.id)
    )
    res = await session.execute(q)
    groups = res.all()
    return [GroupPydantic.from_orm(group) for group in groups]
