import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request

from app.core.config import settings
from app.services.redis_client import RedisClient, get_redis

logger = logging.getLogger(__name__)

WINDOW_SECONDS = 60


async def rate_limit(
    request: Request,
    redis: Annotated[RedisClient | None, Depends(get_redis)],
) -> None:
    if redis is None:
        return

    ip = request.client.host if request.client else "unknown"
    key = f"rl:analyze:{ip}"
    try:
        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, WINDOW_SECONDS)
        if count <= settings.rate_limit_per_minute:
            return
        retry_after = max(await redis.ttl(key), 1)
    except Exception:
        logger.warning("rate limit check failed, allowing request", exc_info=True)
        return

    raise HTTPException(
        status_code=429,
        detail="Too many requests. Please wait a moment and try again.",
        headers={"Retry-After": str(retry_after)},
    )
