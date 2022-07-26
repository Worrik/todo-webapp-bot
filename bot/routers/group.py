from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.chat_type import GroupFilter
from bot.filters.reply_todo import TodoReplyFilter
from bot.models.group import Group
from bot.models.todo import Performer, Tag, Todo
from bot.models.user import User

import sqlalchemy as sa

from bot.utils.parse_todo import parse_tags, parse_users


router = Router(name="group router")
router.message.bind_filter(GroupFilter)


@router.message(commands=["start"])
async def command_start_handler(message: Message) -> None:
    link_button = types.InlineKeyboardButton(
        text="Test", url="https://t.me/todo_webapp_bot"
    )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[link_button]])
    await message.answer("Test", reply_markup=keyboard)


@router.message(commands=["todos_list"])
async def command_todos_list(
    message: Message, group: Group, session: AsyncSession
) -> None:
    q = sa.select(Todo).where(Todo.group_id == group.id)
    res = await session.execute(q)
    todos = res.scalars().unique().all()
    await message.answer("\n".join([t.text for t in todos]))


@router.message(Command(commands=["todo"], commands_prefix="!"))
async def create_todo(
    message: types.Message, session: AsyncSession, user: User, group: Group
) -> None:
    todo_message = message.reply_to_message or message

    text = todo_message.text or ""

    if todo_message == message:
        text = text[6:]

    if not text:
        await message.reply("Error: the message doesn't have text.")
        return

    todo = Todo(
        id=todo_message.message_id,
        creator_id=user.id,
        text=text,
        group_id=group.id,
    )
    session.add(todo)
    await session.commit()

    await message.reply(
        "Successfully create a todo.\n"
        "Now you can add <code>!users</code> or <code>!tags</code>"
        " by replying to a todo message.",
    )


@router.message(
    Command(commands=["user", "users"], commands_prefix="!"), TodoReplyFilter()
)
async def add_users(message: Message, session: AsyncSession):
    todo_message = message.reply_to_message

    if not todo_message:
        return

    todo = await session.get(Todo, todo_message.message_id)
    users = [
        user
        for user in await parse_users(message, session)
        if user not in todo.users
    ]
    session.add_all(
        [Performer(todo_id=todo.id, user_id=user.id) for user in users]
    )
    await session.commit()
    await message.reply(f"Added {len(users)} user(s)")


@router.message(
    Command(commands=["tag", "tags"], commands_prefix="!"), TodoReplyFilter()
)
async def add_tags(message: Message, session: AsyncSession):
    todo_message = message.reply_to_message

    if not todo_message:
        return

    todo = await session.get(Todo, todo_message.message_id)
    tags = [tag.name for tag in todo.tags]
    new_tags = [tag for tag in await parse_tags(message) if tag not in tags]
    session.add_all([Tag(todo_id=todo.id, name=tag) for tag in new_tags])
    await session.commit()
    await message.reply(f"Added {len(new_tags)} tag(s)")


@router.message()
async def echo(_: Message):
    pass
