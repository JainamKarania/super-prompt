import hashlib
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "knowledge"
MAX_CHARS = 2500


def parse_note(path: Path) -> tuple[str, str, str]:
    """Return (title, source, content) for a note written as: '# Title', 'Source: URL', text."""
    lines = path.read_text(encoding="utf-8-sig").strip().splitlines()
    if len(lines) < 3 or not lines[0].startswith("# ") or not lines[1].startswith("Source: "):
        raise ValueError(f"{path.name}: expected '# Title', 'Source: URL', then the note text")
    title = lines[0][2:].strip()
    source = lines[1][len("Source: ") :].strip()
    content = "\n".join(lines[2:]).strip()
    if not content:
        raise ValueError(f"{path.name}: the note has no text")
    if len(content) > MAX_CHARS:
        raise ValueError(f"{path.name}: note is longer than {MAX_CHARS} characters")
    return title, source, content


def content_hash(title: str, content: str) -> str:
    return hashlib.sha256(f"{title}\n{content}".encode()).hexdigest()
