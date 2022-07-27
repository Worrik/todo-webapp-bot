from aiogram.dispatcher.filters.base import BaseFilter
from aiogram.types.message import Message
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.todo import Todo


class IsTodoFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        todo = await session.get(Todo, message.message_id)
        return bool(todo)
