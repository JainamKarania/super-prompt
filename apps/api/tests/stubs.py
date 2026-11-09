from app.schemas import Dimension, TaskType
from app.services.coach import CoachError, CoachOut


class StubCoach:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []
        self.error: CoachError | None = None

    async def coach(self, prompt: str, task: TaskType) -> CoachOut:
        self.calls.append((prompt, task))
        if self.error is not None:
            raise self.error
        return CoachOut(
            dimensions=[
                Dimension(name="clarity", score=2, feedback="clarity feedback"),
                Dimension(name="context", score=4, feedback="context feedback"),
                Dimension(name="constraints", score=6, feedback="constraints feedback"),
                Dimension(name="format", score=8, feedback="format feedback"),
                Dimension(name="examples", score=10, feedback="examples feedback"),
            ],
            improved=f"IMPROVED: {prompt}",
            changes=["Added a role"],
        )
