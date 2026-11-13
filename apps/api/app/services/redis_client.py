from functools import lru_cache
from typing import Any

from redis.asyncio import Redis

from app.core.config import settings

RedisClient = Any


@lru_cache
def get_redis() -> RedisClient | None:
    """One shared client, or None when REDIS_URL is not set."""
    if settings.redis_url is None:
        return None
    return Redis.from_url(
        settings.redis_url.get_secret_value(),
        decode_responses=True,
        socket_timeout=2,
        socket_connect_timeout=2,
    )
