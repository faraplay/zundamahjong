from sqlalchemy.orm import Session

from ..server.sio import sio
from .engine import db_factory


def get_db(sid: str) -> Session:
    with sio.session(sid) as session:
        if "db" not in session:
            session["db"] = db_factory()
        return session["db"]  # type: ignore[no-any-return]


def close_db(sid: str) -> None:
    with sio.session(sid) as session:
        if "db" in session:
            session["db"].close()
