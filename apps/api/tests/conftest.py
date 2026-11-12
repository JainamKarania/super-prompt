import os
from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.models import Base
from app.db.session import get_session
from app.main import app
from app.services.coach import get_coach
from tests.stubs import StubCoach

LOCAL_HOSTS = {"localhost", "127.0.0.1"}


@pytest.fixture
def stub_coach() -> Iterator[StubCoach]:
    stub = StubCoach()
    app.dependency_overrides[get_coach] = lambda: stub
    yield stub
    app.dependency_overrides.pop(get_coach, None)


@pytest.fixture
async def session_maker() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    test_url = os.environ.get("TEST_DATABASE_URL")
    if not test_url:
        pytest.skip("TEST_DATABASE_URL is not set")

    test = make_url(test_url)
    real = make_url(settings.database_url)
    same_database = (test.host, test.port, test.database) == (real.host, real.port, real.database)
    if same_database and test.host not in LOCAL_HOSTS:
        pytest.fail("TEST_DATABASE_URL must not point at your real database")

    engine = create_async_engine(test_url, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


@pytest.fixture
async def client(
    stub_coach: StubCoach, session_maker: async_sessionmaker[AsyncSession]
) -> AsyncIterator[AsyncClient]:
    async def override() -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_session] = override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.pop(get_session, None)
