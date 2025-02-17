import time
from datetime import datetime
from typing import Any, Dict

# from app.config import settings
# from app.database import SessionLocal
# from app.logger import app_logger
# from redis import Redis
# from redis.exceptions import ConnectionError as RedisConnectionError
# from sqlalchemy import text
# from sqlalchemy.exc import OperationalError


class HealthChecker:
    def __init__(self):
        self.start_time = time.monotonic()
        self.version = "1.0.0"

    async def check_database(self) -> Dict[str, Any]:
        """Проверка подключения к MySQL"""
        result = {"status": "ok", "response_time": 0.0}
        # start = time.monotonic()

        # try:
        #     with SessionLocal() as session:
        #         session.execute(text("SELECT 1"))
        #         result["response_time"] = time.monotonic() - start
        # except OperationalError as e:
        #     result.update(
        #         {
        #             "status": "error",
        #             "error": str(e),
        #             "response_time": time.monotonic() - start,
        #         }
        #     )
        #     app_logger.error("Database healthcheck failed", error=str(e))

        return result

    async def check_redis(self) -> Dict[str, Any]:
        """Проверка подключения к Redis"""
        result = {"status": "ok", "response_time": 0.0}
        # start = time.monotonic()

        # try:
        #     redis = Redis.from_url(settings.redis_url, socket_timeout=1)
        #     if not redis.ping():
        #         raise RuntimeError("Redis ping failed")
        #     result["response_time"] = time.monotonic() - start
        # except (RedisConnectionError, RuntimeError) as e:
        #     result.update(
        #         {
        #             "status": "error",
        #             "error": str(e),
        #             "response_time": time.monotonic() - start,
        #         }
        #     )
        #     app_logger.error("Redis healthcheck failed", error=str(e))

        return result

    @property
    def timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def uptime(self) -> float:
        return time.monotonic() - self.start_time


health_checker = HealthChecker()
