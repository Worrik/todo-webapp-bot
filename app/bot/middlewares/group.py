from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.client.bot import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group import Group, GroupUser
from app.models.user import User

import sqlalchemy as sa


class GroupMiddleware(BaseMiddleware):
    async def update_group(
        self, session: AsyncSession, group_id: int, data: dict
    ) -> Group:
        q = sa.update(Group).where(Group.id == group_id)
        q = q.values(**data)
        await session.execute(q)
        group = await session.get(Group, group_id)
        return group

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.chat.type not in ["group"]:
            return await handler(event, data)

        bot: Bot = data["bot"]
        session: AsyncSession = data["session"]
        group: Group = await session.get(Group, event.chat.id)

        if not group:
            chat = await bot.get_chat(event.chat.id)
            photo = None
            if chat.photo:
                file = await bot.get_file(chat.photo.big_file_id)
                if file.file_path:
                    await bot.download_file(
                        file.file_path, f"static/{file.file_unique_id}"
                    )
                    photo = file.file_unique_id
            group_data = chat.dict()
            group_data["photo"] = photo
            group = Group(**group_data)
            session.add(group)

        elif event.new_chat_photo:
            photo_size = event.new_chat_photo[-1]
            file = await bot.get_file(photo_size.file_id)
            if file.file_path:
                await bot.download_file(
                    file.file_path, f"static/{file.file_unique_id}"
                )
                group = await self.update_group(
                    session, group.id, {"photo": file.file_unique_id}
                )

        elif (
            group.type != event.chat.type
            or group.title != event.chat.title
            or group.username != event.chat.username
            or group.description != event.chat.description
            or group.invite_link != event.chat.invite_link
            or group.photo != event.chat.photo
        ):
            group = await self.update_group(
                session,
                group.id,
                dict(
                    type=event.chat.type,
                    title=event.chat.title,
                    username=event.chat.username,
                    description=event.chat.description,
                    invite_link=event.chat.invite_link,
                    photo=event.chat.photo,
                ),
            )

        user: User = data["user"]

        group_user = await session.get(GroupUser, (user.id, group.id))

        if not group_user:
            group_user = GroupUser(user_id=user.id, group_id=group.id)
            session.add(group_user)

        await session.commit()

        data["group"] = group
        data["group_user"] = group_user
        return await handler(event, data)
