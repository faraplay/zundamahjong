import hashlib
import secrets
from typing import Optional

import sqlalchemy as sa

from ..server.player_info import Player
from . import get_db
from .models import User

max_users = 256


def _hash_internal(password: str, salt: str, method: str) -> str:
    method, *args = method.split(":")

    if method != "scrypt":
        raise NotImplementedError

    n, r, p = map(int, args)
    maxmem = 132 * n * r * p

    return hashlib.scrypt(
        password.encode(), salt=salt.encode(), n=n, r=r, p=p, maxmem=maxmem
    ).hex()


def hash_pw(
    password: str, salt: Optional[str] = None, method: Optional[str] = None
) -> str:
    if not salt:
        salt = secrets.token_urlsafe(16)

    if not method:
        method = "scrypt:32768:8:1"

    hashval = _hash_internal(password, salt, method)
    return f"{method}${salt}${hashval}"


def check_pw(password: str, pwhash: str) -> bool:
    method, salt, hashval = pwhash.split("$", 2)
    return hashval == _hash_internal(password, salt, method)


def login(sid: str, name: str, password: str) -> Player:
    db = get_db(sid)

    user = db.execute(sa.select(User).where(User.name == name)).scalar_one_or_none()

    if user:
        if not check_pw(password, user.password):
            raise Exception("Incorrect password!")

        else:
            return Player(name=name, has_account=True)

    elif password:
        num_users = db.scalar(sa.select(sa.func.count(User.id)))

        if num_users and num_users >= max_users:
            raise Exception("Unable to register new user!")

        else:
            db.add(User(name=name, password=hash_pw(password)))
            db.commit()
            return Player(name=name, has_account=True, new_user=True)

    return Player(name=name)


def change_password(
    sid: str, player: Player, cur_password: str, new_password: str
) -> None:
    db = get_db(sid)
    user = db.execute(sa.select(User).where(User.name == player.name)).scalar_one_or_none()

    if user:
        if not check_pw(cur_password, user.password):
            raise Exception("Current password is incorrect!")

        else:
            user.password = hash_pw(new_password)
            db.commit()

    else:
        raise Exception("User does not exist!")
