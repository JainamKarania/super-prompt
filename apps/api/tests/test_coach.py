import pytest
from pydantic import ValidationError

from app.schemas import Dimension, DimensionName
from app.services.coach import CoachOut

ALL: list[DimensionName] = ["clarity", "context", "constraints", "format", "examples"]


def _dim(name: DimensionName) -> Dimension:
    return Dimension(name=name, score=5, feedback="ok")


def test_accepts_one_score_per_dimension() -> None:
    out = CoachOut(dimensions=[_dim(n) for n in ALL], improved="x", changes=[])
    assert len(out.dimensions) == 5


def test_rejects_a_missing_dimension() -> None:
    with pytest.raises(ValidationError):
        CoachOut(dimensions=[_dim(n) for n in ALL[:4]], improved="x", changes=[])


def test_rejects_a_repeated_dimension() -> None:
    dims = [_dim(n) for n in ALL[:4]] + [_dim("clarity")]
    with pytest.raises(ValidationError):
        CoachOut(dimensions=dims, improved="x", changes=[])
