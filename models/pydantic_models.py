from datetime import datetime
from typing import List, Optional
from aiogram import types, Bot

import pydantic


class TagPydantic(pydantic.BaseModel):
    name: str

    class Config:
        orm_mode = True


class TodoPydantic(pydantic.BaseModel):
    id: int
    creator: types.User
    created_at: datetime
    group_id: int
    users: List[types.User]
    tags: List[TagPydantic]
    text: str
    status: Optional[str]

    class Config:
        orm_mode = True


class GroupPydantic(pydantic.BaseModel):
    id: int
    type: Optional[str]
    title: Optional[str]
    username: Optional[str]
    description: Optional[str]
    invite_link: Optional[str]
    photo: Optional[str]

    todos_count: Optional[int]

    class Config:
        orm_mode = True
