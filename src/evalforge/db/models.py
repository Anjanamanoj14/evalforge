from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, Text, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class App(Base):
    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    test_cases: Mapped[list["TestCase"]] = relationship(back_populates="app")
    runs: Mapped[list["Run"]] = relationship(back_populates="app")


class TestCase(Base):
    __tablename__ = "test_cases"
    __test__ = False  # stops pytest from treating this class as a test

    id: Mapped[int] = mapped_column(primary_key=True)
    app_id: Mapped[int] = mapped_column(ForeignKey("apps.id"))
    question: Mapped[str] = mapped_column(Text)
    expected_answer: Mapped[str | None] = mapped_column(Text, default=None)
    source_context: Mapped[str | None] = mapped_column(Text, default=None)

    app: Mapped["App"] = relationship(back_populates="test_cases")
    results: Mapped[list["Result"]] = relationship(back_populates="test_case")


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    app_id: Mapped[int] = mapped_column(ForeignKey("apps.id"))
    model_name: Mapped[str] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    app: Mapped["App"] = relationship(back_populates="runs")
    results: Mapped[list["Result"]] = relationship(back_populates="run")


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id"))
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_cases.id"))
    actual_answer: Mapped[str | None] = mapped_column(Text, default=None)
    retrieved_context: Mapped[str | None] = mapped_column(Text, default=None)
    faithfulness: Mapped[float | None] = mapped_column(Float, default=None)
    relevance: Mapped[float | None] = mapped_column(Float, default=None)
    latency_ms: Mapped[float | None] = mapped_column(Float, default=None)
    prompt_tokens: Mapped[int | None] = mapped_column(Integer, default=None)
    completion_tokens: Mapped[int | None] = mapped_column(Integer, default=None)
    cost_usd: Mapped[float | None] = mapped_column(Float, default=None)

    run: Mapped["Run"] = relationship(back_populates="results")
    test_case: Mapped["TestCase"] = relationship(back_populates="results")