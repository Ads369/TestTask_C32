from typing import AsyncGenerator, Optional

import redis.asyncio as redis
from redis.exceptions import ConnectionError

from app.core.config import settings  # Assumes settings.REDIS_URL is defined
from app.core.exceptions import RedisConnectionError, RedisDataError


class RedisRepository:
    """
    An asynchronous repository for Redis using redis.asyncio.
    Provides basic CRUD operations: get, set, and delete.
    """

    def __init__(self, redis_url: str):
        self._client = redis.from_url(
            settings.REDIS_URL, encoding="utf-8", decode_responses=True
        )

    async def check_connect(self):
        try:
            await self._client.ping()
        except ConnectionError as e:
            raise RedisConnectionError(f"Failed to connect to Redis: {e}")

    async def get(self, key: str) -> Optional[str]:
        return await self._client.get(key)

    async def set(self, key: str, value: str, expire: int | None = None) -> bool:
        if expire is None:
            expire = settings.REDIS_TIMEOUT
        return await self._client.set(key, value, ex=expire)

    async def delete(self, key: str) -> int:
        return await self._client.delete(key)

    async def close(self):
        await self._client.close()


async def get_redis() -> AsyncGenerator[RedisRepository, None]:
    """
    FastAPI dependency
    TODO Здесь нужно подумать о более корректной работе с pools
    """
    repo = RedisRepository(redis_url=settings.REDIS_URL)
    try:
        yield repo
    finally:
        await repo.close()
