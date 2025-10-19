from socketio import Server
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

from ..types.player import Player
from . import get_db, get_user, try_get_user
from .models import User

max_users = 256


def login(sio: Server, sid: str, name: str, password: str) -> Player:
    db = get_db(sio, sid)
    user = try_get_user(db, name)

    if user:
        if not check_password_hash(user.password, password):
            raise Exception("Incorrect password!")

        else:
            return Player(name=name, has_account=True)

    elif password:
        num_users = db.scalar(sa.select(sa.func.count(User.id)))

        if num_users and num_users >= max_users:
            raise Exception("Unable to register new user!")

        else:
            db.add(User(name=name, password=generate_password_hash(password)))
            db.commit()
            return Player(name=name, has_account=True, new_user=True)

    return Player(name=name)


def change_password(
    sio: Server, sid: str, player: Player, cur_password: str, new_password: str
) -> None:
    db = get_db(sio, sid)
    user = get_user(db, player.name)

    if not check_password_hash(user.password, cur_password):
        raise Exception("Current password is incorrect!")

    else:
        user.password = generate_password_hash(new_password)
        db.commit()
