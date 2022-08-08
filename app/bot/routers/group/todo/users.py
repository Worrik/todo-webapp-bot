from aiogram.client.bot import Bot
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.router import Router
from aiogram.types.message import Message
from aiogram.utils.chat_action import ChatActionSender
from sqlalchemy.ext.asyncio.session import AsyncSession
from aiogram.utils.i18n import gettext as _
import sqlalchemy as sa

from app.bot.filters.reply_todo import TodoReplyFilter
from app.bot.utils.parse_todo import parse_users
from app.bot.utils.html_unparse import html_decoration
from app.models.group import Group
from app.models.todo import Performer, Todo
from app.models.user import User


router = Router(name="group todos users")


@router.message(
    Command(commands=["user", "users"], commands_prefix="!"), TodoReplyFilter()
)
async def add_users(
    message: Message, session: AsyncSession, bot: Bot, user: User
):
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

        if todo_message.text and "me" in todo_message.text.split():
            users.append(user)

        session.add_all(
            [
                Performer(
                    todo_id=todo.id,
                    todo_group_id=todo.group_id,
                    user_id=user.id,
                )
                for user in set(users)
            ]
        )
        await session.commit()
        await message.reply(
            _("Added {users_count} user(s)").format(users_count=len(users))
        )


@router.message(
    Command(
        commands=["del-user", "del-users", "delete-user", "delete-users"],
        commands_prefix="!",
    ),
    TodoReplyFilter(),
)
async def delete_users(
    message: Message, session: AsyncSession, bot: Bot, user: User
):
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

        if todo_message.text and "me" in todo_message.text.split():
            users.append(user)

        sa.delete(Performer).where(
            sa.and_(
                Performer.user_id.in_([user.id for user in users]),
                Performer.todo_id == todo.id,
                Performer.todo_group_id == todo.group_id
            )
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

        text = todo_message.text or ""
        text = html_decoration.unparse(text, todo_message.entities)
        text = text.replace("\n", "<br/>")

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
                [
                    Performer(
                        todo_id=todo.id,
                        todo_group_id=todo.group_id,
                        user_id=user.id,
                    )
                    for user in users
                ]
            )
            await session.commit()
            await message.reply(
                _(
                    "Successfully create a todo for {count_users} user(s)\n"
                ).format(count_users=len(users))
            )
