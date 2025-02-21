# import pytest
# import pytest_asyncio
# from app.api.dependencies.databas import get_async_db
# from app.db.base import Base
# from app.main import app
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker

# TEST_DATABASE_URL = "mysql+aiomysql://user:password@mysql_db/testdb"

# engine = create_async_engine(TEST_DATABASE_URL)
# TestingSessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
# )


# @pytest_asyncio.fixture(scope="session")
# async def initialize_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest_asyncio.fixture
# async def session(initialize_db) -> AsyncSession:
#     async with TestingSessionLocal() as session:
#         yield session
#         await session.rollback()


# @pytest_asyncio.fixture
# async def client(session: AsyncSession) -> AsyncClient:
#     async def override_get_db():
#         yield session

#     app.dependency_overrides[get_async_db] = override_get_db
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac
#     app.dependency_overrides.clear()
#
import pytest
import pytest_asyncio
from app.main import app

from .utils import ClientManagerType, client_manager


@pytest_asyncio.fixture(scope="module")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


# @pytest_asyncio.fixture(autouse=True)
# async def clean_db():
#     """
#     Фикстура для очистки базы данных перед каждым тестом, чтобы тесты были независимыми.
#     """
#     for model in Tortoise.apps.get("models", {}).values():
#         await model.all().delete()
