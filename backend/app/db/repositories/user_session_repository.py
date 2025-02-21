from datetime import datetime, timezone

from app.db.models.user_session import UserSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, session_id: str) -> UserSession:
        new_session = UserSession(id=session_id)
        self.session.add(new_session)
        await self.session.commit()
        await self.session.refresh(new_session)
        return new_session

    async def get_by_id(self, session_id: str) -> UserSession | None:
        query = select(UserSession).where(UserSession.id == session_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_last_activity(self, session_id: str) -> None:
        session = await self.get_by_id(session_id)
        if session:
            session.last_activity = datetime.now(timezone.utc)
            await self.session.commit()
