"""add avatar column

Revision ID: 249e8cbf38f8
Create Date: 2025-10-12 22:37:44.772065+00:00

"""
from collections.abc import Sequence
from enum import IntEnum

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e41b71ccd79"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


class Avatar(IntEnum):
    zundamon = 0
    metan = 1
    tsumugi = 2
    kiritan = 3


def upgrade() -> None:
    """Upgrade schema."""
    sa.Enum(Avatar).create(op.get_bind())
    op.add_column(
        "user_account",
        sa.Column("avatar", sa.Enum(Avatar), nullable=False, server_default="zundamon"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user_account", "avatar")
    sa.Enum(Avatar).drop(op.get_bind())
