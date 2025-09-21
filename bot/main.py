import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from bot.config import load_config, Config
from bot.middlewares import DbSessionMiddleware
from bot.handlers.user_handlers import router as user_router


from redis.asyncio import Redis

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')
    engine = create_async_engine(
        "sqlite+aiosqlite:///db.sqlite3",
        echo=True,
        poolclass=NullPool
    )
    config = load_config()
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    bot = Bot(config.tg_bot.bot_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    redis = Redis(host='localhost', port=6379, db=0)
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_router(user_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())