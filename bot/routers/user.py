from aiogram import F, types
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.router import Router
from aiogram.types.message import Message
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.filters.chat_type import PrivateFilter
from bot.models.user import User

import sqlalchemy as sa

router = Router(name="user router")
router.message.bind_filter(PrivateFilter)


@router.message(Command(commands=["start"]))
async def start_command(message: Message, user: User):
    if (
        message.from_user
        and message.from_user.language_code == "ru"
        and not user.verified
    ):
        button = types.KeyboardButton(text=_("Героям слава!"))
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[[button]], resize_keyboard=True
        )
        await message.answer(_("Слава Україні!"), reply_markup=keyboard)
        return
    await message.answer("Hello")


@router.message(F.text == "Героям слава!")
async def verify(message: Message, user: User, session: AsyncSession):
    q = sa.update(User).where(User.id == user.id).values(verified=True)
    await session.execute(q)
    await session.commit()
    await message.answer(
        _("Welcome"),
        reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True),
    )
