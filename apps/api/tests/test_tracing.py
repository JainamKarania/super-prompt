import pytest

from app.core.config import settings
from app.services.tracing import get_callbacks, tracing_enabled


def test_tracing_is_off_without_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "langfuse_public_key", None)
    monkeypatch.setattr(settings, "langfuse_secret_key", None)

    assert tracing_enabled() is False
    assert get_callbacks() == []


def test_tracing_needs_both_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "langfuse_public_key", "pk-lf-test")
    monkeypatch.setattr(settings, "langfuse_secret_key", None)

    assert tracing_enabled() is False
    assert get_callbacks() == []
