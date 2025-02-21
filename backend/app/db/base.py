from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase

from app.core.logger import logger


class Base(DeclarativeBase):
    pass


async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        # Drop all tables (useful in testing)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized")
