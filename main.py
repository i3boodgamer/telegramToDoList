import asyncio
import logging
import sys

from datetime import datetime
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import config
from handlers import user_commands
from handlers.apsched import send_notifications
from middlewares.antiflood import AntiFloodMiddleware
from middlewares.db import DataBaseSession
from database.engine import create_db, async_session


bot = Bot(token=config.BOT_TOKEN)


async def on_startup():
    await create_db()


async def main():
    dp = Dispatcher()

    dp.startup.register(on_startup)

    dp.message.middleware(AntiFloodMiddleware())
    dp.update.middleware(DataBaseSession(session_pool=async_session))

    dp.include_routers(
        user_commands.router,
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_notifications,
        trigger='cron',
        hour=datetime.now().hour,
        minute=datetime.now().minute+1,
        start_date=datetime.now(),
        kwargs={'bot': bot},
    )
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())