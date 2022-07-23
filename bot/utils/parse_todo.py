from typing import List, Tuple
from itertools import chain, groupby
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

    # dict entities grouped by type
    grouped_entities = groupby(message.entities or [], key=attrgetter("type"))
    entities = {k: list(v) for k, v in grouped_entities}

    mentions = entities.get("mention", [])
    text_mentions = entities.get("text_mention", [])
    hashtags = entities.get("hashtag", [])

    # extract usernames from message without '@'
    mentions = [i.extract(message.text)[1:] for i in mentions]

    # select users from db which are in mentions
    q = sa.select(User).where(
        sa.or_(
            User.username.in_(mentions),
            User.id.in_([getattr(e.user, "id") for e in text_mentions]),
        )
    )
    result = await session.execute(q)

    users = list(result.scalars())

    # create users if its exists in db
    usernames = [user.username for user in users]
    new_users_with_usernames = [
        User(username=username)
        for username in mentions
        if username not in usernames
    ]
    session.add_all(new_users_with_usernames)

    ids = [user.id for user in users]
    new_users_without_usernames = [
        User(
            id=e.user.id,
            first_name=e.user.first_name,
            last_name=e.user.last_name,
            is_bot=e.user.is_bot,
            username=e.user.username,
            language_code=e.user.language_code,
        )
        for e in text_mentions
        if e.user and e.user.id not in ids
    ]
    session.add_all(new_users_without_usernames)

    await session.commit()

    tags = [e.extract(message.text)[1:] for e in hashtags]

    users = list(
        chain(users, new_users_with_usernames, new_users_without_usernames)
    )

    return text, tags, users
