from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from app.core.config import settings
from app.core.logger import logger
from app.db.redis import RedisRepository
from app.external.CBRF_client import CBRFClient, CBRFResponse


class CBRFService:
    """Service for fetching and caching CBRF daily rates"""

    def __init__(self, redis: RedisRepository):
        self._redis = redis
        self._cache_ttl = timedelta(hours=1)

    async def get_daily_rates(self) -> Dict[str, Any]:
        """Get daily rates from cache or CBRF API

        Returns:
            Dictionary containing date and exchange rates
        """
        # Try to get from cache first
        cached_data = await self._get_cached_rates()
        if cached_data is not None:
            return cached_data

        # Fetch fresh data if not in cache
        async with CBRFClient() as client:
            rates: CBRFResponse = await client.get_daily_rates()

        # Cache the fresh data
        await self._cache_rates(rates)

        return rates

    async def _get_cached_rates(self) -> Optional[Dict[str, Any]]:
        """Get rates from cache if available"""
        try:
            data = await self._redis.get(settings.REDIS_USD_KEY)
            if data:
                return data
        except Exception as e:
            logger.error(f"Error getting rates from cache: {e}")
        return None

    async def _cache_rates(self, rates: CBRFResponse) -> None:
        """Cache rates"""
        try:
            await self._redis.set(
                settings.REDIS_DATA_KEY,
                rates["Date"],
                expire=int(self._cache_ttl.total_seconds()),
            )
            await self._redis.set(
                settings.REDIS_USD_KEY,
                str(rates["Valute"]),
                expire=int(self._cache_ttl.total_seconds()),
            )
        except Exception as e:
            logger.error(f"Error caching rates: {e}")
