from datetime import datetime

from aiogram import Bot
from sqlalchemy import select

from database.engine import async_session
from database.models import Task


async def get_due_tasks():
    async with async_session() as db:
        now = datetime.now()
        print(datetime.utcnow())
        result = await db.execute(select(Task).where(Task.due_date <= now))
        tasks = result.scalars().all()
        return tasks


async def send_notifications(bot: Bot):
    tasks = await get_due_tasks()
    for task in tasks:
        await bot.send_message(task.user_id, f"Напоминание: {task.description}")

