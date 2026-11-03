from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppCreate(BaseModel):
    name: str
    description: str | None = None


class AppOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime


class TestCaseCreate(BaseModel):
    __test__ = False

    question: str
    expected_answer: str | None = None
    source_context: str | None = None


class TestCaseOut(BaseModel):
    __test__ = False
    model_config = ConfigDict(from_attributes=True)

    id: int
    app_id: int
    question: str
    expected_answer: str | None
    source_context: str | None