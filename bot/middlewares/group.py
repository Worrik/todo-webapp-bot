from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.group import Group


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
            await session.commit()

        data["group"] = group
        return await handler(event, data)
