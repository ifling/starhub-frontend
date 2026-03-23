"""users table and activity owner_user_id

Revision ID: 0003_users_and_owner
Revises: 0002_activity_creator_id
Create Date: 2026-03-19

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0003_users_and_owner"
down_revision = "0002_activity_creator_id"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel", sa.String(length=16), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.Column("openid", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("channel", "openid", name="uq_users_channel_openid"),
    )
    op.create_index(op.f("ix_users_channel"), "users", ["channel"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_openid"), "users", ["openid"], unique=False)

    op.add_column(
        "activities",
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_activities_owner_user_id_users",
        "activities",
        "users",
        ["owner_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(op.f("ix_activities_owner_user_id"), "activities", ["owner_user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_activities_owner_user_id"), table_name="activities")
    op.drop_constraint("fk_activities_owner_user_id_users", "activities", type_="foreignkey")
    op.drop_column("activities", "owner_user_id")

    op.drop_index(op.f("ix_users_openid"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_channel"), table_name="users")
    op.drop_table("users")
