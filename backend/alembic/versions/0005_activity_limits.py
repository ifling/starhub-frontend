"""add activities.limits json

Revision ID: 0005_activity_limits
Revises: 0004_users_username
Create Date: 2026-03-26

"""

from alembic import op
import sqlalchemy as sa


revision = "0005_activity_limits"
down_revision = "0004_users_username"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("activities", sa.Column("limits", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("activities", "limits")

