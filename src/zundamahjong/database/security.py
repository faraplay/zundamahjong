import hashlib
import secrets
from typing import Optional

import sqlalchemy as sa

from ..types.player import Player
from . import db
from .models import User
from .users import get_user, try_get_user

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
    try:
        method, salt, hashval = pwhash.split("$", 2)
    except ValueError:
        raise Exception("Malformed password hash.")

    return hashval == _hash_internal(password, salt, method)


def login(name: str, password: str) -> Player:
    with db.session.begin():
        user = try_get_user(name)

        if user:
            if not check_pw(password, user.password):
                raise Exception("Incorrect password!")

            else:
                return Player(name=name, has_account=True)

        elif password:
            num_users = db.session.scalar(sa.select(sa.func.count(User.id)))

            if num_users and num_users >= max_users:
                raise Exception("Unable to register new user!")

            else:
                db.session.add(User(name=name, password=hash_pw(password)))

                return Player(name=name, has_account=True, new_user=True)

        return Player(name=name)


def change_password(player: Player, cur_password: str, new_password: str) -> None:
    with db.session.begin():
        user = get_user(player.name)

        if not check_pw(cur_password, user.password):
            raise Exception("Current password is incorrect!")

        else:
            user.password = hash_pw(new_password)
