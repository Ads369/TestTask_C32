from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.exceptions import DatabaseError
from app.core.logger import logger

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL_ASYNC,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


# async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
#     """Async dependency providing database session"""

#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#             await session.commit()
#         except SQLAlchemyError as exc:
#             await session.rollback()
#             logger.error("Database session rollback: %s", exc)
#             raise DatabaseError() from exc
#         finally:
#             await session.close()
