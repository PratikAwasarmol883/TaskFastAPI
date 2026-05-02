import re

from pydantic import BaseModel, Field, StrictStr, field_validator

_NOSQL_OPERATOR_RE = re.compile(r"\$\w+")


class RequestTask(BaseModel):
    model_config = {"extra": "forbid"}

    taskName: StrictStr = Field(min_length=1, max_length=200)
    whatYouLearnt: StrictStr = Field(min_length=5, max_length=2000)

    @field_validator("taskName", "whatYouLearnt")
    @classmethod
    def _reject_nosql_operators(cls, value: str) -> str:
        if _NOSQL_OPERATOR_RE.search(value):
            raise ValueError("Input must not contain NoSQL operators")
        return value
