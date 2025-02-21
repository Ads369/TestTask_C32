from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.databas import get_async_db
from app.db.repositories.user_session_repository import UserSessionRepository


async def validate_user_session(
    request: Request, db: AsyncSession = Depends(get_async_db)
) -> str:
    try:
        session_id = request.state.session_id
        session_repo = UserSessionRepository(db)
        session = await session_repo.get_by_id(session_id)

        if not session:
            session = await session_repo.create(session_id)

        await session_repo.update_last_activity(session_id)

        return session_id
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No session found"
        )
