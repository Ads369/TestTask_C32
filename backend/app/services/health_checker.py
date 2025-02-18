import time
from datetime import datetime
from typing import Any, Dict, Union

from app.db.redis import RedisRepository
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class HealthChecker:
    """
    Integration test for the system
    """

    def __init__(self):
        self.start_time = time.monotonic()
        self.version = "1.0.0"

    async def check_database(self, db: Union[Session, AsyncSession]) -> Dict[str, Any]:
        """Проверка подключения к MySQL"""
        try:
            if isinstance(db, Session):
                _ = db.execute(text("SELECT 1"))
            else:
                _ = await db.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}

    async def check_redis(self, redis: RedisRepository) -> Dict[str, Any]:
        """Проверка подключения к Redis"""
        try:
            _ = await redis.check_connect()
            return {"status": "ok", "database": "connected"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}

    @property
    def timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def uptime(self) -> float:
        return time.monotonic() - self.start_time


health_checker = HealthChecker()
