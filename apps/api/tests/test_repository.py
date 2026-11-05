from app.db.repository import prompt_hash


def test_prompt_hash_ignores_case_and_whitespace() -> None:
    assert prompt_hash("Write  a Blog", "writing") == prompt_hash("write a blog", "writing")


def test_prompt_hash_depends_on_task() -> None:
    assert prompt_hash("hi", "writing") != prompt_hash("hi", "code")
