import logging
import hashlib
import os
import secrets

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from ..server.sio import sio

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)


engine = create_engine("sqlite:///debug.db")
db_factory = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


if not os.path.isfile("debug.db"):
    create_tables()


def get_db(sid: str) -> Session:
    with sio.session(sid) as session:
        if "db" not in session:
            session["db"] = db_factory()
        return session["db"]


def _hash_internal(password: str, salt: str, method: str) -> str:
    method, *args = method.split(":")

    if method != "scrypt":
        raise NotImplementedError

    n, r, p = map(int, args)
    maxmem = 132 * n * r * p

    return hashlib.scrypt(
        password.encode(), salt=salt.encode(), n=n, r=r, p=p, maxmem=maxmem
    ).hex()


def hash_pw(password: str, salt: str | None, method: str | None) -> str:
    if not salt:
        salt = secrets.token_urlsafe(16)

    if not method:
        method = "scrypt:32768:8:1"

    hashval = _hash_internal(password, salt, method)
    return f"{method}${salt}${hashval}"


def check_pw(password: str, pwhash: str) -> bool:
    method, salt, hashval = pwhash.split("$", 2)
    return hashval == _hash_internal(password, salt, method)
