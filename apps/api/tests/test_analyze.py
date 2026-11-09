import uuid

from httpx import AsyncClient

from app.services.coach import CoachError, CoachRateLimited
from tests.stubs import StubCoach

BODY = {"prompt": "write a blog", "task": "writing"}


async def test_analyze_uses_the_coach_result(client: AsyncClient, stub_coach: StubCoach) -> None:
    r = await client.post("/api/analyze", json=BODY)
    assert r.status_code == 200
    body = r.json()
    assert body["original"] == "write a blog"
    assert body["improved"] == "IMPROVED: write a blog"
    assert body["overall"] == 6.0
    assert len(body["dimensions"]) == 5
    assert "createdAt" in body
    assert stub_coach.calls == [("write a blog", "writing")]


async def test_empty_prompt_never_reaches_the_coach(
    client: AsyncClient, stub_coach: StubCoach
) -> None:
    r = await client.post("/api/analyze", json={"prompt": "", "task": "writing"})
    assert r.status_code == 422
    assert stub_coach.calls == []


async def test_whitespace_prompt_is_rejected(client: AsyncClient) -> None:
    r = await client.post("/api/analyze", json={"prompt": "   ", "task": "writing"})
    assert r.status_code == 422


async def test_unknown_task_is_rejected(client: AsyncClient) -> None:
    r = await client.post("/api/analyze", json={"prompt": "hi", "task": "poetry"})
    assert r.status_code == 422


async def test_analysis_is_saved_and_can_be_fetched(client: AsyncClient) -> None:
    created = (await client.post("/api/analyze", json=BODY)).json()
    r = await client.get(f"/api/analyses/{created['id']}")
    assert r.status_code == 200
    assert r.json()["original"] == "write a blog"


async def test_list_returns_newest_first(client: AsyncClient) -> None:
    await client.post("/api/analyze", json={**BODY, "prompt": "first"})
    await client.post("/api/analyze", json={**BODY, "prompt": "second"})
    items = (await client.get("/api/analyses")).json()
    assert [i["original"] for i in items] == ["second", "first"]


async def test_unknown_id_returns_404(client: AsyncClient) -> None:
    r = await client.get(f"/api/analyses/{uuid.uuid4()}")
    assert r.status_code == 404


async def test_malformed_id_returns_422(client: AsyncClient) -> None:
    r = await client.get("/api/analyses/not-a-uuid")
    assert r.status_code == 422


async def test_rate_limited_model_returns_429_and_saves_nothing(
    client: AsyncClient, stub_coach: StubCoach
) -> None:
    stub_coach.error = CoachRateLimited("slow down")
    r = await client.post("/api/analyze", json=BODY)
    assert r.status_code == 429
    assert (await client.get("/api/analyses")).json() == []


async def test_failed_model_returns_502_and_saves_nothing(
    client: AsyncClient, stub_coach: StubCoach
) -> None:
    stub_coach.error = CoachError("bad output")
    r = await client.post("/api/analyze", json=BODY)
    assert r.status_code == 502
    assert (await client.get("/api/analyses")).json() == []
