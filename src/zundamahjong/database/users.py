from typing import Optional

import sqlalchemy as sa

from . import db
from .models import User


def get_user(name: str) -> User:
    return db.session.execute(sa.select(User).where(User.name == name)).scalar_one()


def try_get_user(name: str) -> Optional[User]:
    return db.session.execute(
        sa.select(User).where(User.name == name)
    ).scalar_one_or_none()
