from aiogram import types
from aiogram.client.bot import Bot
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.router import Router
from aiogram.types.message import Message
from aiogram.utils.i18n import gettext as _

from app.bot.filters.chat_type import PrivateFilter
from app.config import WEB_APP_URL


router = Router(name="user router")
router.message.bind_filter(PrivateFilter)


@router.message(Command(commands=["start"]))
async def start_command(message: Message, bot: Bot):
    web_app_info = types.WebAppInfo(url=WEB_APP_URL)
    web_app_button = types.InlineKeyboardButton(
        text="Todos", web_app=web_app_info
    )
    info_button = types.InlineKeyboardButton(
        text=_("How to use"),
        url=_("https://telegra.ph/How-to-use-TODO-Bot-08-10"),
    )
    add_to_group_button = types.InlineKeyboardButton(
        text=_("Add to group"),
        url="https://t.me/todo_webapp_bot?startgroup=true",
    )
    support_button = types.InlineKeyboardButton(
        text=_("Support"), url="https://t.me/worrik"
    )
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [web_app_button, info_button],
            [add_to_group_button, support_button],
        ]
    )
    await message.answer(
        _(
            "Hello! I'm a TODO bot. Here are some valuable "
            "links and a Todos button."
        ),
        reply_markup=keyboard,
    )

    await bot.set_chat_menu_button(
        message.chat.id,
        types.MenuButtonWebApp(
            type="web_app", text="Todos", web_app=web_app_info
        ),
    )


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
