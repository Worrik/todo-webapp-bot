from aiogram import types
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.router import Router
from aiogram.types.message import Message

from bot.filters.chat_type import PrivateFilter
from config import WEB_APP_URL

router = Router(name="user router")
router.message.bind_filter(PrivateFilter)


@router.message(Command(commands=["start"]))
async def start_command(message: Message):
    web_app_button = types.InlineKeyboardButton(
        text="Web App", web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])
    await message.answer("Hello", reply_markup=keyboard)
