from aiogram import types
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.router import Router
from aiogram.types.message import Message
from aiogram.utils.i18n import gettext as _

from app.bot.filters.chat_type import PrivateFilter
from app.config import WEB_APP_URL


router = Router(name="user router")
router.message.bind_filter(PrivateFilter)


@router.message(Command(commands=["start"]))
async def start_command(message: Message):
    web_app_button = types.InlineKeyboardButton(
        text="Todos", web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    info_button = types.InlineKeyboardButton(
        text=_("How to use"), url=_("how_to_use_url")
    )
    add_to_group_button = types.InlineKeyboardButton(
        text=_("Add to group"),
        url="https://t.me/todo_webapp_bot?startgroup=true",
    )
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[web_app_button, info_button], [add_to_group_button]]
    )
    await message.answer("Hello", reply_markup=keyboard)


@router.message(commands=["help"])
async def command_start_handler(message: Message) -> None:
    await message.answer(
        _(
            "Commands:\n"
            "<code>!todo</code> - create a todo.\n"
            "<code>!user</code> or <code>!users</code> - add user(s).\n"
            "<code>!tag</code> or <code>!tags</code> - add tag(s).\n"
            "<code>!del</code> or <code>!delete</code> - delete a todo."
        )
    )
