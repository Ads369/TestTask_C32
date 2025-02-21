import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        cookie_name: str = "session_id",
        cookie_max_age: int = 86400,  # 24 hours in seconds
    ):
        super().__init__(app)
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        session_id = request.cookies.get("session_id") or request.headers.get(
            "X-Session-ID"
        )

        if not session_id:
            session_id = str(uuid.uuid4())

        request.state.session_id = session_id

        response = await call_next(request)

        response.set_cookie("session_id", session_id)
        response.headers["X-Session-ID"] = session_id

        return response
