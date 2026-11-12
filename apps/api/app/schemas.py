from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from pydantic.alias_generators import to_camel

TaskType = Literal["writing", "code", "analysis"]
DimensionName = Literal["clarity", "context", "constraints", "format", "examples"]


class AnalyzeRequest(BaseModel):
    prompt: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    task: TaskType


class Dimension(BaseModel):
    name: DimensionName
    score: float = Field(ge=0, le=10)
    feedback: str


class Technique(BaseModel):
    title: str
    source: str


class Analysis(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str
    created_at: str
    original: str
    improved: str
    overall: float = Field(ge=0, le=10)
    dimensions: list[Dimension]
    changes: list[str]
    techniques: list[Technique] = Field(default_factory=list)
