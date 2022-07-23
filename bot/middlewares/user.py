from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User

import sqlalchemy as sa


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user:
            session: AsyncSession = data["session"]
            user = await session.get(User, event.from_user.id)

            if not user:
                q = (
                    sa.select(User)
                    .where(User.username == event.from_user.username)
                    .limit(1)
                )
                res = await session.execute(q)
                user = res.scalar()

                if user:
                    q = sa.update(User).where(User.username == user.username)
                    q = q.values(
                        id=event.from_user.id,
                        first_name=event.from_user.first_name,
                        last_name=event.from_user.last_name,
                        is_bot=event.from_user.is_bot,
                        username=event.from_user.username,
                        language_code=event.from_user.language_code,
                    )
                    await session.execute(q)
                    user = await session.get(User, event.from_user.id)

                else:
                    user = User(
                        id=event.from_user.id,
                        first_name=event.from_user.first_name,
                        last_name=event.from_user.last_name,
                        is_bot=event.from_user.is_bot,
                        username=event.from_user.username,
                        language_code=event.from_user.language_code,
                    )

                    session.add(user)
                    await session.commit()

            data["user"] = user
        return await handler(event, data)
