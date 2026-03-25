import datetime as dt
import uuid

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("channel", "openid", name="uq_users_channel_openid"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # web | weixin_mp | qq_mp
    channel: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    openid: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )

    activities: Mapped[list["Activity"]] = relationship(back_populates="owner")


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(12), unique=True, index=True, nullable=False)

    creator_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)

    owner_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )

    title: Mapped[str] = mapped_column(String(120), nullable=False)
    type: Mapped[str] = mapped_column(String(24), nullable=False, default="副本")
    deadline_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    desc: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )

    owner: Mapped["User | None"] = relationship(back_populates="activities")

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

