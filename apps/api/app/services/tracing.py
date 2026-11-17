import logging
import os
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)


def tracing_enabled() -> bool:
    return bool(settings.langfuse_public_key and settings.langfuse_secret_key)


def get_callbacks() -> list[Any]:
    """LangChain callbacks for Langfuse, or [] when tracing is not configured.

    Tracing must never break a request, so any failure here is logged and ignored.
    """
    if not tracing_enabled():
        return []
    try:
        # Langfuse reads its configuration from environment variables, but our
        # .env file is only loaded into Settings, so pass the values along.
        assert settings.langfuse_public_key is not None
        assert settings.langfuse_secret_key is not None
        os.environ.setdefault("LANGFUSE_PUBLIC_KEY", settings.langfuse_public_key)
        os.environ.setdefault(
            "LANGFUSE_SECRET_KEY", settings.langfuse_secret_key.get_secret_value()
        )
        os.environ.setdefault("LANGFUSE_BASE_URL", settings.langfuse_base_url)

        from langfuse.langchain import CallbackHandler

        return [CallbackHandler()]
    except Exception:
        logger.warning("could not set up Langfuse tracing", exc_info=True)
        return []
