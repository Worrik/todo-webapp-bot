from aiogram.dispatcher.filters.base import BaseFilter
from aiogram.types.chat import Chat
from aiogram.types.message import Message


class ChatTypeFilter(BaseFilter):
    chat_type: str

    async def __call__(self, _: Message, event_chat: Chat) -> bool:
        if event_chat:
            return event_chat.type == self.chat_type
        return False


class GroupFilter(ChatTypeFilter):
    chat_type: str = "group"


class PrivateFilter(ChatTypeFilter):
    chat_type: str = "private"
