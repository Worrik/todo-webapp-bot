from datetime import datetime
from typing import List, Optional
from aiogram import types

import pydantic


class OrmModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


class TagPydantic(OrmModel):
    name: str


class StatusPydantic(OrmModel):
    name: Optional[str]


class UserPydantic(OrmModel):
    id: int
    is_bot: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or ""


class TodoPydantic(OrmModel):
    id: int
    creator: types.User
    created_at: datetime
    group_id: int
    users: List[UserPydantic]
    tags: List[TagPydantic]
    text: str
    status: Optional[StatusPydantic]


class GroupPydantic(OrmModel):
    id: int
    type: Optional[str]
    title: Optional[str]
    username: Optional[str]
    description: Optional[str]
    invite_link: Optional[str]
    photo: Optional[str]

    todos_count: Optional[int]
