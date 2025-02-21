"""Exception handler setup for FastAPI application.

This module provides setup for handling different types of exceptions in the FastAPI application:
- AppException: Custom application exceptions
- HTTPException: FastAPI HTTP exceptions
- Exception: Generic fallback handler for unhandled exceptions

Each handler:
- Logs the exception with request ID
- Returns appropriate status code and error message
- Includes request ID in response for support reference
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.logger import logger


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def custom_exception_handler(request: Request, exc: AppException):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(
            f"Application error for RequestID: {request_id}. Exception: {exc}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": f"{exc.detail}. Please contact support with RequestID: {request_id}"
            },
        )

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

    @app.exception_handler(HTTPException)
    async def fastapi_exception_handler(request: Request, exc: HTTPException):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(
            f"FastAPI error for RequestID: {request_id}. Exception: {exc}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": f"{exc.detail}. Please contact support with RequestID: {request_id}"
            },
        )
