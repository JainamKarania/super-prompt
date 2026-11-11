import math
from functools import lru_cache
from typing import Protocol

from app.core.config import EMBEDDING_DIM

MODEL_NAME = "BAAI/bge-small-en-v1.5"


class Embedder(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class FastEmbedder:
    def __init__(self) -> None:
        from fastembed import TextEmbedding  # imported here so app startup stays fast

        self._model = TextEmbedding(model_name=MODEL_NAME)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [vector.tolist() for vector in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


@lru_cache
def get_embedder() -> Embedder:
    return FastEmbedder()


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm


__all__ = ["EMBEDDING_DIM", "Embedder", "FastEmbedder", "cosine", "get_embedder"]
