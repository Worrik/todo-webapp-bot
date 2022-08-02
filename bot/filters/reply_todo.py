from aiogram.dispatcher.filters.base import BaseFilter
from aiogram.types.message import Message
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.todo import Todo


class TodoReplyFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if message.reply_to_message:
            todo = await session.get(
                Todo, (message.reply_to_message.message_id, message.chat.id)
            )
            return bool(todo)
        return False
