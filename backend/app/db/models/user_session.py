from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String

from app.db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String(36), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_activity = Column(DateTime, default=datetime.now(timezone.utc))
