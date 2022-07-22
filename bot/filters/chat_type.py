from aiogram.dispatcher.filters.base import BaseFilter
from aiogram.types.chat import Chat
from aiogram.types.message import Message


class GroupFilter(BaseFilter):
    chat_type: str = "group"

    async def __call__(self, _: Message, event_chat: Chat) -> bool:
        if event_chat:
            return event_chat.type == self.chat_type
        return False
