import uuid

from httpx import AsyncClient

BODY = {"prompt": "write a blog", "task": "writing"}


async def test_analyze_returns_all_dimensions(client: AsyncClient) -> None:
    r = await client.post("/api/analyze", json=BODY)
    assert r.status_code == 200
    body = r.json()
    assert len(body["dimensions"]) == 5
    assert body["original"] == "write a blog"
    assert "createdAt" in body
    assert 0 <= body["overall"] <= 10


async def test_analyze_rejects_empty_prompt(client: AsyncClient) -> None:
    r = await client.post("/api/analyze", json={"prompt": "", "task": "writing"})
    assert r.status_code == 422


async def test_analyze_rejects_whitespace_prompt(client: AsyncClient) -> None:
    r = await client.post("/api/analyze", json={"prompt": "   ", "task": "writing"})
    assert r.status_code == 422


async def test_analyze_rejects_unknown_task(client: AsyncClient) -> None:
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
