from aiogram.dispatcher.router import Router

from app.bot.filters.chat_type import GroupFilter
from . import info, todo


router = Router(name="group router")
router.message.bind_filter(GroupFilter)
router.edited_message.bind_filter(GroupFilter)

router.include_router(info.router)
router.include_router(todo.router)


__all__ = ("router",)
