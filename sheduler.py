from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def start_scheduler():
    scheduler.start()


def schedule_task(task_id, run_date, description):
    scheduler.add_job(
        func=send_reminder,
        trigger='date',
        run_date=run_date,
        args=[task_id, description]
    )


async def send_reminder(task_id, description):
    pass
