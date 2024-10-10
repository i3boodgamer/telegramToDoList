from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


from database.engine import async_session


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_session):
        self.sessionPool = session_pool

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        async with self.sessionPool() as session:
            data['session'] = session
            return await handler(event, data)
