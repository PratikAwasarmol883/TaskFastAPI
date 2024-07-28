from pydantic import BaseModel, Field


class RequestTask(BaseModel):
    taskName: str
    whatYouLearnt: str = Field(min_length=5)