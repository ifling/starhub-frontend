"""add activity creator_id

Revision ID: 0002_activity_creator_id
Revises: 0001_init
Create Date: 2026-03-18

"""

from alembic import op
import sqlalchemy as sa


revision = "0002_activity_creator_id"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("activities", sa.Column("creator_id", sa.String(length=64), nullable=False, server_default=""))
    op.create_index("ix_activities_creator_id", "activities", ["creator_id"], unique=False)
    op.alter_column("activities", "creator_id", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_activities_creator_id", table_name="activities")
    op.drop_column("activities", "creator_id")

