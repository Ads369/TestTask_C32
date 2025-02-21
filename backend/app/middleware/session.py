from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

# from app.db.models.user_session import UserSession


async def session_middleware(request: Request, call_next: RequestResponseEndpoint):
    # Получаем session_id из куки
    session_id = request.cookies.get("session_id")

    if not session_id:
        # Создаем новую сессию
        session_id = str(uuid4())
    else:
        # Обновляем время последней активности

        response = await call_next(request)

    return response
