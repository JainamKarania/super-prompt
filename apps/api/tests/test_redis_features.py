from collections.abc import AsyncIterator

import fakeredis.aioredis
import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.schemas import TaskType
from app.services.cache import CachedCoach
from app.services.coach import CoachOut
from app.services.ratelimit import rate_limit
from app.services.redis_client import RedisClient, get_redis
from tests.stubs import StubCoach


class CountingCoach:
    """Wraps the stub coach and counts how often it is really called."""

    def __init__(self) -> None:
        self.calls = 0
        self._stub = StubCoach()

    async def coach(self, prompt: str, task: TaskType) -> CoachOut:
        self.calls += 1
        return await self._stub.coach(prompt, task)


class BrokenRedis:
    async def get(self, key: str) -> None:
        raise ConnectionError("redis is down")

    async def set(self, *args: object, **kwargs: object) -> None:
        raise ConnectionError("redis is down")


@pytest.fixture
def fake_redis() -> RedisClient:
    return fakeredis.aioredis.FakeRedis(decode_responses=True)


async def test_second_identical_call_is_served_from_cache(
    fake_redis: RedisClient,
) -> None:
    inner = CountingCoach()
    coach = CachedCoach(inner, fake_redis)

    first = await coach.coach("Write a blog post", "writing")
    second = await coach.coach("  Write a blog post  ", "writing")

    assert inner.calls == 1
    assert second == first


async def test_different_task_is_a_different_cache_entry(
    fake_redis: RedisClient,
) -> None:
    inner = CountingCoach()
    coach = CachedCoach(inner, fake_redis)

    await coach.coach("Write a blog post", "writing")
    await coach.coach("Write a blog post", "code")

    assert inner.calls == 2


async def test_without_redis_every_call_goes_through() -> None:
    inner = CountingCoach()
    coach = CachedCoach(inner, None)

    await coach.coach("Write a blog post", "writing")
    await coach.coach("Write a blog post", "writing")

    assert inner.calls == 2


async def test_redis_failure_does_not_break_the_coach() -> None:
    inner = CountingCoach()
    coach = CachedCoach(inner, BrokenRedis())

    out = await coach.coach("Write a blog post", "writing")

    assert out is not None
    assert inner.calls == 1


@pytest.fixture
async def limited_client(
    fake_redis: RedisClient, monkeypatch: pytest.MonkeyPatch
) -> AsyncIterator[AsyncClient]:
    monkeypatch.setattr(settings, "rate_limit_per_minute", 2)
    app = FastAPI()

    @app.get("/ping", dependencies=[Depends(rate_limit)])
    async def ping() -> dict[str, bool]:
        return {"ok": True}

    app.dependency_overrides[get_redis] = lambda: fake_redis
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def test_rate_limit_blocks_after_the_limit(limited_client: AsyncClient) -> None:
    assert (await limited_client.get("/ping")).status_code == 200
    assert (await limited_client.get("/ping")).status_code == 200

    blocked = await limited_client.get("/ping")

    assert blocked.status_code == 429
    assert int(blocked.headers["retry-after"]) >= 1
