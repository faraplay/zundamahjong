from typing import Optional

from socketio import Server  # type: ignore[import-untyped]
import sqlalchemy as sa
from sqlalchemy.orm import Session

from .engine import db_factory
from .models import User


def get_db(sio: Server, sid: str) -> Session:
    with sio.session(sid) as session:
        if "db" not in session:
            session["db"] = db_factory()
        return session["db"]  # type: ignore[no-any-return]


def close_db(sio: Server, sid: str) -> None:
    with sio.session(sid) as session:
        if "db" in session:
            session["db"].close()


def get_user(db: Session, name: str) -> Optional[User]:
    return db.execute(sa.select(User).where(User.name == name)).scalar_one_or_none()
