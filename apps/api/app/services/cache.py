import hashlib
import logging

from app.core.config import settings
from app.schemas import TaskType
from app.services.coach import Coach, CoachOut
from app.services.redis_client import RedisClient

logger = logging.getLogger(__name__)

# Bump this whenever the scoring or rewrite prompts change,
# so old cached answers are not served for new behaviour.
CACHE_VERSION = "v1"


class CachedCoach:
    def __init__(self, inner: Coach, redis: RedisClient | None, ttl: int | None = None) -> None:
        self._inner = inner
        self._redis = redis
        self._ttl = ttl if ttl is not None else settings.cache_ttl_seconds

    def _key(self, prompt: str, task: TaskType) -> str:
        digest = hashlib.sha256(prompt.strip().encode()).hexdigest()
        return f"coach:{CACHE_VERSION}:{settings.llm_model}:{task}:{digest}"

    async def coach(self, prompt: str, task: TaskType) -> CoachOut:
        if self._redis is None:
            return await self._inner.coach(prompt, task)

        key = self._key(prompt, task)
        try:
            hit = await self._redis.get(key)
            if hit is not None:
                return CoachOut.model_validate_json(hit)
        except Exception:
            logger.warning("cache read failed", exc_info=True)

        out = await self._inner.coach(prompt, task)
        try:
            await self._redis.set(key, out.model_dump_json(), ex=self._ttl)
        except Exception:
            logger.warning("cache write failed", exc_info=True)
        return out
