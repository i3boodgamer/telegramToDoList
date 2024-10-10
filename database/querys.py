import logging
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import Select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Task


async def add_item(
        item: Dict[str, Any],
        user_id: int,
        session: AsyncSession
) -> None:
    try:
        queries = Task(
            description=item["description"],
            user_id=user_id,
            due_date=datetime.strptime(item["date"], "%Y-%m-%d %H:%M")
        )
        session.add(queries)
        await session.commit()
    except Exception as e:
        logging.info(f"Данные не коретны. Ошибка {e}")
        logging.info(f"Данные: {item}")


async def get_list(
        user_id: int,
        session: AsyncSession
):
    query = await session.execute(
        Select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.id)
    )

    return query.scalars().all()


async def del_list(
        list_id: int,
        session: AsyncSession
):
    post_delete = await  session.get(Task, list_id)
    if post_delete:
        await session.delete(post_delete)
        await session.commit()

