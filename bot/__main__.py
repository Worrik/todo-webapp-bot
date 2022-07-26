from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.middlewares.db import DBMiddleware
from bot.config import DATABASE_URL, TOKEN, logger
from bot.middlewares.group import GroupMiddleware
from bot.middlewares.user import UserMiddleware
from bot.routers import group


dp = Dispatcher()


def main() -> None:
    bot = Bot(TOKEN, parse_mode="html")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    dp.message.outer_middleware(DBMiddleware(async_session))
    dp.message.outer_middleware(UserMiddleware())
    group.router.message.outer_middleware(GroupMiddleware())

    dp.include_router(group.router)

    logger.info("Start")
    dp.run_polling(bot)
    logger.info("Stop")


if __name__ == "__main__":
    main()
