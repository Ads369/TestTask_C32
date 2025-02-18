from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.db.base import init_db
from app.db.mysql import async_engine
from app.middleware.exception_handler import setup_exception_handlers
from app.middleware.logging import LoggingMiddleware

app = FastAPI()

# Add the logging middleware
app.add_middleware(LoggingMiddleware)
setup_exception_handlers(app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(async_engine)
    yield


app.include_router(api_router, prefix="/api")
