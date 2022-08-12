from aiogram import Bot, Dispatcher, types
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio

from app.bot.middlewares.db import DBMiddleware
from app.config import DATABASE_URL, TOKEN, ADMIN_ID
from app.bot.middlewares.group import GroupMiddleware
from app.bot.middlewares.user import UserMiddleware
from app.bot.routers import group, user


dp = Dispatcher()


async def on_startup(bot: Bot):
    commands = [types.BotCommand(command="help", description="Help")]
    await bot.set_my_commands(commands)


async def error_handler(exception: Exception, bot: Bot):
    error = f"{exception}, {exception.args}"
    await bot.send_message(ADMIN_ID, error)


async def main() -> None:
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
        observer.middleware(group_middleware)

    dp.include_router(user.router)
    dp.include_router(group.router)
    dp.register_errors

    print("Run on_startup")
    await on_startup(bot)
    print("Start")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stop")
