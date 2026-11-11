from pathlib import Path

import pytest

from app.services.embedder import EMBEDDING_DIM, FastEmbedder, cosine
from app.services.knowledge import KNOWLEDGE_DIR, content_hash, parse_note

GOOD = "# A title\nSource: https://example.com\n\nSome text about prompts.\n"


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "note.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_parse_note_reads_title_source_and_content(tmp_path: Path) -> None:
    title, source, content = parse_note(_write(tmp_path, GOOD))
    assert title == "A title"
    assert source == "https://example.com"
    assert content == "Some text about prompts."


def test_parse_note_rejects_a_missing_source(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        parse_note(_write(tmp_path, "# A title\n\nSome text\nmore text\n"))


def test_parse_note_rejects_a_very_long_note(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        parse_note(_write(tmp_path, GOOD + "x" * 3000))


def test_content_hash_changes_when_the_text_changes() -> None:
    assert content_hash("t", "a") != content_hash("t", "b")
    assert content_hash("t", "a") == content_hash("t", "a")


def test_every_real_note_is_valid() -> None:
    paths = sorted(KNOWLEDGE_DIR.glob("*.md"))
    assert len(paths) >= 10
    for path in paths:
        parse_note(path)


@pytest.mark.embedding
def test_embedder_returns_the_right_size_and_ranks_similar_text_higher() -> None:
    embedder = FastEmbedder()
    question, similar, unrelated = embedder.embed_documents(
        [
            "How do I say what format the answer should have?",
            "Tell the model whether you want bullets, a table, or JSON.",
            "The capital of France is Paris.",
        ]
    )
    assert len(question) == EMBEDDING_DIM
    assert cosine(question, similar) > cosine(question, unrelated)
