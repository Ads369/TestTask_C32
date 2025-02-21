from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI

from app.api import api_router
from app.core.scheduler import DeliveryCostScheduler
from app.db.base import init_db
from app.db.mysql import AsyncSessionLocal, async_engine
from app.middleware.exception_handler import setup_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.middleware.session import SessionMiddleware
from app.seed.package_types import seed_package_types

scheduler: Optional[DeliveryCostScheduler] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO тут должен быть Alembic или его аналоги
    await init_db(async_engine)
    await seed_package_types()

    # Start scheduler
    global scheduler
    scheduler = DeliveryCostScheduler(AsyncSessionLocal)
    await scheduler.start()

    yield

    # Stop scheduler
    if scheduler:
        await scheduler.stop()


app = FastAPI(lifespan=lifespan)

# Add the logging middleware
app.add_middleware(SessionMiddleware)
app.add_middleware(LoggingMiddleware)
setup_exception_handlers(app)


app.include_router(api_router, prefix="/api")
