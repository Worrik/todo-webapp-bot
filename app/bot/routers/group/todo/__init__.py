from aiogram.dispatcher.router import Router
from . import base, users

router = Router(name="group todos")
router.include_router(base.router)
router.include_router(users.router)

__all__ = ("router",)
