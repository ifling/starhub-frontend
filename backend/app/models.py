import datetime as dt
import uuid

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(12), unique=True, index=True, nullable=False)

    title: Mapped[str] = mapped_column(String(120), nullable=False)
    type: Mapped[str] = mapped_column(String(24), nullable=False, default="副本")
    deadline_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    desc: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )

    signups: Mapped[list["Signup"]] = relationship(
        back_populates="activity",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Signup(Base):
    __tablename__ = "signups"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    nickname: Mapped[str] = mapped_column(String(64), nullable=False)
    role: Mapped[str | None] = mapped_column(String(16), nullable=True)  # tank/healer/dps/other
    note: Mapped[str | None] = mapped_column(String(200), nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )

    activity: Mapped[Activity] = relationship(back_populates="signups")


Index("ix_signups_activity_created_at", Signup.activity_id, Signup.created_at)

