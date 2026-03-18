"""init

Revision ID: 0001_init
Revises: 
Create Date: 2026-03-18

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=12), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("type", sa.String(length=24), nullable=False),
        sa.Column("deadline_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("desc", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_activities_code"), "activities", ["code"], unique=False)

    op.create_table(
        "signups",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("activity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nickname", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=True),
        sa.Column("note", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_signups_activity_id"), "signups", ["activity_id"], unique=False)
    op.create_index("ix_signups_activity_created_at", "signups", ["activity_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_signups_activity_created_at", table_name="signups")
    op.drop_index(op.f("ix_signups_activity_id"), table_name="signups")
    op.drop_table("signups")

    op.drop_index(op.f("ix_activities_code"), table_name="activities")
    op.drop_table("activities")

