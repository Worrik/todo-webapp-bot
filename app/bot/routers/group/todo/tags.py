from aiogram.client.bot import Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.reply_todo import TodoReplyFilter
from app.bot.utils.parse_todo import parse_tags
from app.models.todo import Tag, Todo

import sqlalchemy as sa


router = Router(name="todo's tags")


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
            [
                Tag(todo_id=todo.id, todo_group_id=todo.group_id, name=tag)
                for tag in set(new_tags)
            ]
        )
        await session.commit()
        await message.reply(
            _("Added {tags_count} tag(s)").format(tags_count=len(new_tags))
        )


@router.message(
    Command(
        commands=["del-tag", "del-tags", "delete-tag", "delete-tags"],
        commands_prefix="!",
    ),
    TodoReplyFilter(),
)
async def delete_tags(message: Message, session: AsyncSession, bot: Bot):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        todo_message = message.reply_to_message

        if not todo_message:
            return

        todo = await session.get(
            Todo, (todo_message.message_id, todo_message.chat.id)
        )
        tags = [tag.name for tag in todo.tags]
        del_tags = [tag for tag in await parse_tags(message) if tag in tags]
        q = sa.delete(Tag)
        q = q.where(
            sa.and_(
                Tag.name.in_(del_tags),
                Todo.id == todo.id,
                Todo.group_id == Todo.group_id,
            )
        )
        q = q.returning(Tag.id)
        res = await session.execute(q)
        await session.commit()
        await message.reply(
            _("Deleted {tags_count} tag(s)").format(tags_count=len(res.all()))
        )
