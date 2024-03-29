from aiogram import F, types
from aiogram.client.bot import Bot
from aiogram.dispatcher.router import Router
from aiogram.types.message import Message
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio.session import AsyncSession

import sqlalchemy as sa

from app.models.group import Group, GroupUser


router = Router(name="group info")


@router.message(commands=["start", "help"])
async def command_start_handler(message: Message) -> None:
    link_to_bot_button = types.InlineKeyboardButton(
        text=_("Chat with bot"), url="https://t.me/todo_webapp_bot"
    )
    how_to_use_button = types.InlineKeyboardButton(
        text=_("How to use"), url=_("how_to_use_url")
    )
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[link_to_bot_button, how_to_use_button]]
    )
    await message.answer(
        _(
            "Commands:\n"
            "<code>!todo</code> - create a todo.\n"
            "<code>!user</code> or <code>!users</code> - add user(s).\n"
            "<code>!tag</code> or <code>!tags</code> - add tag(s).\n"
            "<code>!del</code> or <code>!delete</code> - delete a todo."
        ),
        reply_markup=keyboard,
    )


@router.message(F.new_chat_members)
async def new_chat_members(message: Message, session: AsyncSession):
    if not message.new_chat_members:
        return

    group_users = [
        GroupUser(user_id=user.id, group_id=message.chat.id)
        for user in message.new_chat_members
    ]
    session.add_all(group_users)
    await session.commit()


@router.message(F.left_chat_member)
async def left_chat_member(message: Message, session: AsyncSession):
    if not message.left_chat_member:
        return

    q = sa.delete(GroupUser)
    q = q.where(GroupUser.user_id == message.left_chat_member.id)
    q = q.where(GroupUser.group_id == message.chat.id)
    await session.execute(q)
    await session.commit()


@router.message(F.new_chat_title)
async def new_chat_title(
    message: Message, session: AsyncSession, group: Group
):
    group.title = message.new_chat_title or ""
    session.add(group)
    await session.commit()


@router.message(F.new_chat_photo)
async def new_chat_photo(
    message: Message, bot: Bot, session: AsyncSession, group: Group
):
    if not message.new_chat_photo:
        return

    photo_size = message.new_chat_photo[-1]
    file = await bot.get_file(photo_size.file_id)
    if file.file_path:
        await bot.download_file(
            file.file_path, f"static/{file.file_unique_id}"
        )
        group.photo = file.file_unique_id
        session.add(group)
        await session.commit()
