from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from models.group import Group, GroupUser
from models.user import User

import sqlalchemy as sa


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

        elif (
            group.type != event.chat.type
            or group.title != event.chat.title
            or group.username != event.chat.username
            or group.description != event.chat.description
            or group.invite_link != event.chat.invite_link
            or group.photo != event.chat.photo
        ):
            q = sa.update(Group).where(Group.id == group.id)
            q = q.values(
                type=event.chat.type,
                title=event.chat.title,
                username=event.chat.username,
                description=event.chat.description,
                invite_link=event.chat.invite_link,
                photo=event.chat.photo,
            )
            await session.execute(q)
            group = await session.get(Group, event.chat.id)

        user: User = data["user"]

        group_user = await session.get(GroupUser, (user.id, group.id))

        if not group_user:
            group_user = GroupUser(user_id=user.id, group_id=group.id)
            session.add(group_user)

        await session.commit()

        data["group"] = group
        data["group_user"] = group_user
        return await handler(event, data)
