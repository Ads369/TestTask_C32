from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DatabaseError
from app.core.logger import logger
from app.db.mysql import AsyncSessionLocal


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Async dependency providing database session"""

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.error("Database session rollback: %s", exc)
            raise DatabaseError() from exc
        finally:
            await session.close()
