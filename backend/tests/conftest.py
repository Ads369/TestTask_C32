# tests/conftest.py
from typing import AsyncGenerator

import pytest
from app.db.mysql import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a transactional scope around a series of operations.
    For a real-world application, consider creating a separate test database.
    """
    async with AsyncSessionLocal() as session:
        yield session
        # Optionally, you might want to rollback after each test to ensure a clean state:
        await session.rollback()


### Skip integration test by default
def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: mark test as integration test")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-integration"):
        skip_integration = pytest.mark.skip(
            reason="need --run-integration option to run"
        )
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
