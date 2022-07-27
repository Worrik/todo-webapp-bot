from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from models.group import Group, GroupUser
from models.user import User


class GroupMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        group = await session.get(Group, event.chat.id)

        if not group:
            group = Group(**event.chat.dict())

            session.add(group)

        user: User = data["user"]

        group_user = await session.get(GroupUser, (user.id, group.id))

        if not group_user:
            group_user = GroupUser(user_id=user.id, group_id=group.id)
            session.add(group_user)

        await session.commit()

        data["group"] = group
        data["group_user"] = group_user
        return await handler(event, data)
