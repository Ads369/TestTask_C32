import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Generate uuid for each request
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Calculate RequestTime
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Request-Time"] = str(process_time)

        logger.info(
            f"{request.method} {request.url} completed in {process_time:.4f} sec. RequestID: {request_id}"
        )
        return response
