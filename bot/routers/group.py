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
from bot.utils.parse_todo import parse_todo

import sqlalchemy as sa


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
    text, tags, users = await parse_todo(message, session)
    await message.answer(text)

    todo = Todo(
        creator_id=user.id,
        text=text,
        message_id=message.message_id,
        group_id=group.id,
    )
    session.add(todo)
    await session.commit()
    session.add_all([Tag(name=tag, todo_id=todo.id) for tag in tags])
    session.add_all(
        [Performer(user_id=user.id, todo_id=todo.id) for user in users]
    )
    await session.commit()


@router.message(TodoReplyFilter())
async def test(message: Message):
    await message.answer("here")


@router.message()
async def echo(_: Message):
    pass
