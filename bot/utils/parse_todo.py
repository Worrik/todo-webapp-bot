from typing import List, Optional, Tuple
from itertools import groupby
from operator import attrgetter

from aiogram.types.message import Message
from sqlalchemy.ext.asyncio.session import AsyncSession

import sqlalchemy as sa

from bot.models.user import User


async def parse_todo(
    message: Message, session: AsyncSession
) -> Tuple[str, List[str], List[User]]:
    """
    :return: text of todo, list of tags and list of users
    """
    if not message.text:
        raise ValueError("Message doesn't have text")

    text = message.text[6:]
    entities = dict(groupby(message.entities or [], key=attrgetter("type")))

    mentions = entities.get("mention", [])
    text_mentions = entities.get("text_mention", [])
    hashtags = entities.get("hashtag", [])

    mentions = [i.extract(message.text) for i in mentions]

    print(mentions, text_mentions, hashtags)

    q = sa.select(User).where(
        sa.or_(
            User.username.in_(mentions),
            User.id.in_([getattr(e.user, "id") for e in text_mentions]),
        )
    )
    result = await session.execute(q)
    users = result.scalars()

    tags = [e.extract(message.text)[1:] for e in hashtags]

    return text, tags, users
