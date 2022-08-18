from aiogram.dispatcher.router import Router
from . import base, users, tags

router = Router(name="group todos")
router.include_router(base.router)
router.include_router(users.router)
router.include_router(tags.router)

__all__ = ("router",)
