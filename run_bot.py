from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.middlewares.db import DBMiddleware
from config import DATABASE_URL, TOKEN
from bot.middlewares.group import GroupMiddleware
from bot.middlewares.user import UserMiddleware
from bot.routers import group, user


dp = Dispatcher()


def main() -> None:
    bot = Bot(TOKEN, parse_mode="html")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    i18n = I18n(path="locales", default_locale="en", domain="messages")

    i18n_middleware = SimpleI18nMiddleware(i18n)
    db_middleware = DBMiddleware(async_session)
    user_middleware = UserMiddleware()
    group_middleware = GroupMiddleware()

    for event in ["message", "edited_message"]:
        observer = getattr(dp, event)
        observer.outer_middleware(db_middleware)
        observer.outer_middleware(user_middleware)
        observer.middleware(i18n_middleware)

        router_observer = getattr(group.router, event)
        router_observer.middleware(group_middleware)

    dp.include_router(group.router)
    dp.include_router(user.router)

    dp.run_polling(bot)


if __name__ == "__main__":
    main()
