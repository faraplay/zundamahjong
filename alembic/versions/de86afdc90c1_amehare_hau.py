"""amehare hau

Revision ID: de86afdc90c1
Revises: 9e41b71ccd79
Create Date: 2025-10-16 05:01:03.825292+00:00

"""

from enum import IntEnum
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "de86afdc90c1"
down_revision: Union[str, Sequence[str], None] = "9e41b71ccd79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


class OldAvatar(IntEnum):
    zundamon = 0
    metan = 1
    tsumugi = 2
    kiritan = 3


class NewAvatar(IntEnum):
    zundamon = 0
    metan = 1
    tsumugi = 2
    kiritan = 3
    hau = 4


old_avatar = sa.Enum(OldAvatar, name="avatar")
tmp_avatar = sa.Enum(NewAvatar, name="_avatar")
new_avatar = sa.Enum(NewAvatar, name="avatar")

user_table = sa.sql.table(
    "user_account", sa.Column("avatar", new_avatar, nullable=False)
)


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "user_account",
        "avatar",
        server_default=None,
    )
    tmp_avatar.create(op.get_bind())
    op.alter_column(
        "user_account",
        "avatar",
        type_=tmp_avatar,
        postgresql_using="avatar::text::_avatar",
    )
    old_avatar.drop(op.get_bind())
    new_avatar.create(op.get_bind())
    op.alter_column(
        "user_account",
        "avatar",
        type_=new_avatar,
        postgresql_using="avatar::text::avatar",
        server_default="zundamon",
    )
    tmp_avatar.drop(op.get_bind())


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        user_table.update()
        .where(user_table.c.avatar == NewAvatar.hau)
        .values(avatar=NewAvatar.zundamon)
    )
    op.alter_column(
        "user_account",
        "avatar",
        server_default=None,
    )
    tmp_avatar.create(op.get_bind())
    op.alter_column(
        "user_account",
        "avatar",
        type_=tmp_avatar,
        postgresql_using="avatar::text::_avatar",
    )
    new_avatar.drop(op.get_bind())
    old_avatar.create(op.get_bind())
    op.alter_column(
        "user_account",
        "avatar",
        type_=old_avatar,
        postgresql_using="avatar::text::avatar",
        server_default="zundamon",
    )
    tmp_avatar.drop(op.get_bind())
