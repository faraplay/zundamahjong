import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

from ..types.player import Player
from . import db
from .users import get_user, try_get_user
from .models import User

max_users = 256


def login(name: str, password: str) -> Player:
    with db.session.begin():
        user = try_get_user(name)

        if user:
            if not check_password_hash(user.password, password):
                raise Exception("Incorrect password!")

            else:
                return Player(name=name, has_account=True)

        elif password:
            num_users = db.session.scalar(sa.select(sa.func.count(User.id)))

            if num_users and num_users >= max_users:
                raise Exception("Unable to register new user!")

            else:
                db.session.add(
                    User(name=name, password=generate_password_hash(password))
                )

                return Player(name=name, has_account=True, new_user=True)

        return Player(name=name)


def change_password(player: Player, cur_password: str, new_password: str) -> None:
    with db.session.begin():
        user = get_user(player.name)

        if not check_password_hash(user.password, cur_password):
            raise Exception("Current password is incorrect!")

        else:
            user.password = generate_password_hash(new_password)
