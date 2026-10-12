"""Storage for checks and feedback. Only redacted text is ever written."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


def _now():
    return datetime.now(timezone.utc)


class Check(Base):
    __tablename__ = "checks"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)
    channel: Mapped[str] = mapped_column(String(16))          # web, web-image, whatsapp
    language: Mapped[str] = mapped_column(String(4))
    verdict: Mapped[str] = mapped_column(String(16), index=True)
    score: Mapped[float] = mapped_column(Float)
    rule_score: Mapped[float] = mapped_column(Float)
    model_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    flags: Mapped[str] = mapped_column(Text)                  # JSON list of flag ids
    redacted_text: Mapped[str] = mapped_column(Text)


class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    check_id: Mapped[str] = mapped_column(ForeignKey("checks.id"), index=True)
    correct: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Store:
    def __init__(self, url: str):
        kwargs = {"connect_args": {"check_same_thread": False}} if url.startswith("sqlite") else {"pool_pre_ping": True}
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        self.engine = create_engine(url, **kwargs)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(self.engine, expire_on_commit=False)

    def save_check(self, *, channel: str, report: dict, redacted: str) -> str:
        row = Check(
            channel=channel, language=report["message_language"], verdict=report["verdict"],
            score=report["score"], rule_score=report["rule_score"], model_probability=report["model_probability"],
            flags=json.dumps([f["id"] for f in report["flags"]]), redacted_text=redacted,
        )
        with self.session() as s:
            s.add(row)
            s.commit()
        return row.id

    def save_feedback(self, check_id: str, correct: bool) -> bool:
        with self.session() as s:
            if s.get(Check, check_id) is None:
                return False
            s.add(Feedback(check_id=check_id, correct=correct))
            s.commit()
        return True

    def stats(self) -> dict:
        with self.session() as s:
            by_verdict = dict(s.execute(select(Check.verdict, func.count()).group_by(Check.verdict)).all())
            fb = dict(s.execute(select(Feedback.correct, func.count()).group_by(Feedback.correct)).all())
        return {"checks": by_verdict, "feedback": {"correct": fb.get(True, 0), "wrong": fb.get(False, 0)}}

    def labelled_examples(self, session: Session | None = None) -> list[tuple[str, int]]:
        """Redacted texts with a label implied by feedback, for retraining."""
        with self.session() as s:
            rows = s.execute(select(Check.redacted_text, Check.verdict, Feedback.correct).join(Feedback)).all()
        out = []
        for text, verdict, correct in rows:
            flagged = verdict != "no_signs"
            out.append((text, int(flagged == correct)))
        return out
