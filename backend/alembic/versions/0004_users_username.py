"""add users.username for web login

Revision ID: 0004_users_username
Revises: 0003_users_and_owner
Create Date: 2026-03-25

"""

from alembic import op
import sqlalchemy as sa


revision = "0004_users_username"
down_revision = "0003_users_and_owner"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=255), nullable=True))
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.execute(
        sa.text(
            """
            UPDATE users
            SET username = lower(email)
            WHERE channel = 'web' AND email IS NOT NULL AND username IS NULL
            """
        )
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_column("users", "username")
