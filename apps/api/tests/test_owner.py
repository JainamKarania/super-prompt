from httpx import AsyncClient

OTHER_OWNER = "22222222-2222-4222-8222-222222222222"
BODY = {"prompt": "write a blog about coffee", "task": "writing"}


async def test_owners_cannot_see_each_others_analyses(client: AsyncClient) -> None:
    created = await client.post("/api/analyze", json=BODY)
    assert created.status_code == 200
    analysis_id = created.json()["id"]

    mine = await client.get("/api/analyses")
    theirs = await client.get("/api/analyses", headers={"X-Owner-Id": OTHER_OWNER})

    assert [a["id"] for a in mine.json()] == [analysis_id]
    assert theirs.json() == []


async def test_other_owner_gets_404_for_my_analysis(client: AsyncClient) -> None:
    analysis_id = (await client.post("/api/analyze", json=BODY)).json()["id"]

    mine = await client.get(f"/api/analyses/{analysis_id}")
    theirs = await client.get(f"/api/analyses/{analysis_id}", headers={"X-Owner-Id": OTHER_OWNER})

    assert mine.status_code == 200
    assert theirs.status_code == 404


async def test_missing_owner_header_is_rejected(client: AsyncClient) -> None:
    del client.headers["X-Owner-Id"]

    response = await client.get("/api/analyses")

    assert response.status_code == 422


async def test_malformed_owner_header_is_rejected(client: AsyncClient) -> None:
    response = await client.get("/api/analyses", headers={"X-Owner-Id": "not-a-uuid"})

    assert response.status_code == 422
