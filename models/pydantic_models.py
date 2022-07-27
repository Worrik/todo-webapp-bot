from typing import List
from aiogram import types

import pydantic


class TagPydantic(pydantic.BaseModel):
    name: str

    class Config:
        orm_mode = True


class TodoPydantic(pydantic.BaseModel):
    id: int
    creator_id: int
    group_id: int
    users: List[types.User]
    tags: List[TagPydantic]
    text: str

    class Config:
        orm_mode = True
