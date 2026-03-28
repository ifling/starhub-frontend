"""activity_signup_events for signup/cancel log

Revision ID: 0006_activity_signup_events
Revises: 0005_activity_limits
Create Date: 2026-03-28

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0006_activity_signup_events"
down_revision = "0005_activity_limits"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activity_signup_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("activity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("signup_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=16), nullable=False),
        sa.Column("nickname", sa.String(length=64), nullable=False),
        sa.Column("note", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_activity_signup_events_activity_id"), "activity_signup_events", ["activity_id"])
    op.create_index(op.f("ix_activity_signup_events_signup_id"), "activity_signup_events", ["signup_id"])
    op.create_index(
        "ix_activity_signup_events_activity_created_at",
        "activity_signup_events",
        ["activity_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_activity_signup_events_activity_created_at", table_name="activity_signup_events")
    op.drop_index(op.f("ix_activity_signup_events_signup_id"), table_name="activity_signup_events")
    op.drop_index(op.f("ix_activity_signup_events_activity_id"), table_name="activity_signup_events")
    op.drop_table("activity_signup_events")
