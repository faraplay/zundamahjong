from typing import Optional

from socketio import Server
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from .engine import engine
from .models import Base as Base, User

session_factory = sessionmaker(engine)


def get_db(sio: Server, sid: str) -> Session:
    with sio.session(sid) as session:
        if "db" not in session:
            session["db"] = session_factory()
        return session["db"]  # type: ignore[no-any-return]


def close_db(sio: Server, sid: str) -> None:
    with sio.session(sid) as session:
        if "db" in session:
            session["db"].close()


def get_user(db: Session, name: str) -> User:
    return db.execute(sa.select(User).where(User.name == name)).scalar_one()


def try_get_user(db: Session, name: str) -> Optional[User]:
    return db.execute(sa.select(User).where(User.name == name)).scalar_one_or_none()
