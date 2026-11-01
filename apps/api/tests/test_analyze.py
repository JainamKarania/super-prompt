from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_analyze_returns_all_dimensions() -> None:
    r = client.post("/api/analyze", json={"prompt": "write a blog", "task": "writing"})
    assert r.status_code == 200
    body = r.json()
    assert len(body["dimensions"]) == 5
    assert body["original"] == "write a blog"
    assert "createdAt" in body
    assert 0 <= body["overall"] <= 10


def test_analyze_rejects_empty_prompt() -> None:
    r = client.post("/api/analyze", json={"prompt": "", "task": "writing"})
    assert r.status_code == 422


def test_analyze_rejects_whitespace_prompt() -> None:
    r = client.post("/api/analyze", json={"prompt": "   ", "task": "writing"})
    assert r.status_code == 422


def test_analyze_rejects_unknown_task() -> None:
    r = client.post("/api/analyze", json={"prompt": "hi", "task": "poetry"})
    assert r.status_code == 422
