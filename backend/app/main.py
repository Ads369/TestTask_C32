from fastapi import FastAPI

from app.api import api_router
from app.middleware.exception_handler import setup_exception_handlers
from app.middleware.logging import LoggingMiddleware

app = FastAPI()

# Add the logging middleware
app.add_middleware(LoggingMiddleware)
setup_exception_handlers(app)


app.include_router(api_router, prefix="/api")
