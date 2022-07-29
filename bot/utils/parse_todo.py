from typing import Dict, List
from itertools import chain, groupby
from operator import attrgetter

from aiogram.types.message import Message
from aiogram.types.message_entity import MessageEntity
from sqlalchemy.ext.asyncio.session import AsyncSession

import sqlalchemy as sa

from models.user import User


def get_entities_dict(message: Message) -> Dict[str, List[MessageEntity]]:
    # dict entities grouped by type
    grouped_entities = groupby(message.entities or [], key=attrgetter("type"))
    entities = {k: list(v) for k, v in grouped_entities}
    return entities


def get_or_create_users(
    users: List[User],
    session: AsyncSession,
    mentions: List[str],
    text_mentions: List[MessageEntity],
) -> List[User]:
    # create users if its exists in db
    usernames = [user.username for user in users]
    new_users_with_usernames = [
        User(username=username)
        for username in mentions
        if username not in usernames
    ]

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
    session.add_all(new_users_with_usernames)
    session.add_all(new_users_without_usernames)
    users = list(
        chain(users, new_users_with_usernames, new_users_without_usernames)
    )
    return users


async def parse_users(message: Message, session: AsyncSession) -> List[User]:
    """
    get users from message and create if not exists
    :return: list of users
    """
    if not message.text:
        raise ValueError("Message doesn't have text")

    entities = get_entities_dict(message)
    mentions = entities.get("mention", [])
    text_mentions = entities.get("text_mention", [])

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
    users = get_or_create_users(users, session, mentions, text_mentions)

    await session.commit()

    return users


async def parse_tags(message: Message) -> List[str]:
    """
    :return: list of tags
    """
    if not message.text:
        raise ValueError("Message doesn't have text")

    entities = get_entities_dict(message)

    hashtags = entities.get("hashtag", [])

    tags = [e.extract(message.text)[1:] for e in hashtags]

    return tags
