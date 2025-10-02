import hashlib
import secrets

from sqlalchemy import select

from .models import User
from . import get_db


def _hash_internal(password: str, salt: str, method: str) -> str:
    method, *args = method.split(":")

    if method != "scrypt":
        raise NotImplementedError

    n, r, p = map(int, args)
    maxmem = 132 * n * r * p

    return hashlib.scrypt(
        password.encode(), salt=salt.encode(), n=n, r=r, p=p, maxmem=maxmem
    ).hex()


def hash_pw(password: str, salt: str | None = None, method: str | None = None) -> str:
    if not salt:
        salt = secrets.token_urlsafe(16)

    if not method:
        method = "scrypt:32768:8:1"

    hashval = _hash_internal(password, salt, method)
    return f"{method}${salt}${hashval}"


def check_pw(password: str, pwhash: str) -> bool:
    method, salt, hashval = pwhash.split("$", 2)
    return hashval == _hash_internal(password, salt, method)


def login(sid: str, name: str, password: str):
    db = get_db(sid)

    user = db.execute(select(User).where(User.name == name)).scalar_one_or_none()

    if user:
        if not check_pw(password, user.password):
            raise Exception("Incorrect password!")

    elif password:
        db.add(User(name=name, password=hash_pw(password)))
        db.commit()
