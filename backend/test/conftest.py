# tests/conftest.py
import pytest
from app.db.mysql import AsyncSessionLocal  # your async session factory
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="function")
async def async_session() -> AsyncSession:
    """
    Provide a transactional scope around a series of operations.
    For a real-world application, consider creating a separate test database.
    """
    async with AsyncSessionLocal() as session:
        yield session
        # Optionally, you might want to rollback after each test to ensure a clean state:
        await session.rollback()
