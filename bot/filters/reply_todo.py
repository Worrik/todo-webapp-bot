from aiogram.dispatcher.filters.base import BaseFilter
from aiogram.types.message import Message
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from bot.models.todo import Todo

import sqlalchemy as sa


class TodoReplyFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if message.reply_to_message:
            q = sa.select(func.count(Todo.id)).where(
                Todo.message_id == message.reply_to_message.message_id
            )
            res = await session.execute(q)
            return res.scalar()
        return False
