from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.logger import logger


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(
            f"Unhandled error for RequestID: {request_id}. Exception: {exc}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Internal server error. Please contact support with RequestID: {request_id}"
            },
        )
