from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import config
from .models import Base

engine = create_async_engine(url=config.DB_URL, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)