from aiogram.client.bot import Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.chat_type import GroupFilter
from bot.filters.is_todo import IsTodoFilter
from bot.filters.reply_todo import TodoReplyFilter
from models.group import Group
from models.todo import Performer, Status, Tag, Todo
from models.user import User

import sqlalchemy as sa

from bot.utils.parse_todo import parse_tags, parse_users


router = Router(name="group router")
router.message.bind_filter(GroupFilter)
router.edited_message.bind_filter(GroupFilter)


@router.message(commands=["start", "help"])
async def command_start_handler(message: Message) -> None:
    link_button = types.InlineKeyboardButton(
        text=_("Chat with bot"), url="https://t.me/todo_webapp_bot"
    )
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[link_button]])
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


@router.message(Command(commands=["todo"], commands_prefix="!"))
async def create_todo(
    message: types.Message,
    session: AsyncSession,
    user: User,
    group: Group,
    bot: Bot,
) -> None:
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        todo_message = message.reply_to_message or message

        text = todo_message.text or ""

        if todo_message == message:
            text = text[6:]

        if not text:
            await message.reply(_("Error: the message doesn't have text."))
            return

        todo = Todo(
            id=todo_message.message_id,
            creator_id=user.id,
            text=text,
            group_id=group.id,
        )
        session.add(todo)

        try:
            await session.commit()
        except sa.exc.IntegrityError:
            await message.reply(_("Already created todo from this message"))
        else:
            await message.reply(
                _(
                    "Successfully create a todo.\n"
                    "Now you can add <code>!users</code> or <code>!tags</code>"
                    " by replying to a todo message.",
                )
            )


@router.message(
    Command(commands=["user", "users"], commands_prefix="!"), TodoReplyFilter()
)
async def add_users(message: Message, session: AsyncSession, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        todo_message = message.reply_to_message

        if not todo_message:
            return

        todo = await session.get(
            Todo, (todo_message.message_id, todo_message.chat.id)
        )
        users = [
            user
            for user in await parse_users(message, session)
            if user not in todo.users
        ]
        session.add_all(
            [Performer(todo_id=todo.id, user_id=user.id) for user in users]
        )
        await session.commit()
        await message.reply(
            _("Added {users_count} user(s)").format(users_count=len(users))
        )


@router.message(
    Command(commands=["todo-for", "todo-user"], commands_prefix="!"),
)
async def create_todo_for_user(
    message: Message, session: AsyncSession, bot: Bot, user: User, group: Group
):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        todo_message = message.reply_to_message

        if not todo_message:
            return

        text = todo_message.text

        if not text:
            await message.reply(_("Error: the message doesn't have text."))
            return

        todo = Todo(
            id=todo_message.message_id,
            creator_id=user.id,
            text=text,
            group_id=group.id,
        )
        session.add(todo)

        try:
            await session.commit()
        except sa.exc.IntegrityError:
            await message.reply(_("Already created todo from this message"))
        else:
            users = [user for user in await parse_users(message, session)]
            session.add_all(
                [Performer(todo_id=todo.id, user_id=user.id) for user in users]
            )
            await session.commit()
            await message.reply(
                _(
                    "Successfully create a todo for {count_users} user(s)\n"
                ).format(count_users=len(users))
            )


@router.message(
    Command(commands=["tag", "tags"], commands_prefix="!"), TodoReplyFilter()
)
async def add_tags(message: Message, session: AsyncSession, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        todo_message = message.reply_to_message

        if not todo_message:
            return

        todo = await session.get(
            Todo, (todo_message.message_id, todo_message.chat.id)
        )
        tags = [tag.name for tag in todo.tags]
        new_tags = [
            tag for tag in await parse_tags(message) if tag not in tags
        ]
        session.add_all(
            [Tag(todo_id=todo.id, name=tag) for tag in set(new_tags)]
        )
        await session.commit()
        await message.reply(
            _("Added {tags_count} tag(s)").format(tags_count=len(new_tags))
        )


@router.message(
    Command(commands=["del", "delete"], commands_prefix="!"), TodoReplyFilter()
)
async def delete_todo(message: Message, session: AsyncSession, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        todo_message = message.reply_to_message

        if not todo_message:
            return

        todo = await session.get(
            Todo, (todo_message.message_id, todo_message.chat.id)
        )
        await session.delete(todo)
        await session.commit()
        await message.reply(_("Successfully deleted this todo"))


@router.message(
    Command(commands=["status"], commands_prefix="!"), TodoReplyFilter()
)
async def get_or_set_todo_status(
    message: Message, session: AsyncSession, bot: Bot
):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        todo_message = message.reply_to_message

        if not todo_message or not message.text:
            return

        todo: Todo = await session.get(
            Todo, (todo_message.message_id, todo_message.chat.id)
        )

        message_status = message.text.split("!status", maxsplit=1)[-1].strip()

        if not message_status:
            await message.reply(
                todo.status.name or _("Todo doesn't have the status.")
            )
        else:
            q = sa.select(Status).where(Status.name.ilike(message_status))
            status = await session.scalar(q)

            if not status:
                status = Status(name=message_status)
                session.add(status)

            todo.status = status
            session.add(todo)
            await session.commit()
            await message.reply(
                _("Successfully set status: {status}").format(message_status)
            )


@router.edited_message(IsTodoFilter())
async def edit_todo(edited_message: Message, session: AsyncSession):
    text = edited_message.text or ""
    if text.startswith("!todo"):
        text = text[6:]
    q = (
        sa.update(Todo)
        .where(Todo.id == edited_message.message_id)
        .where(Todo.group_id == edited_message.chat.id)
        .values(text=text)
    )
    await session.execute(q)
    await session.commit()


@router.message()
async def echo(_: Message):
    pass
