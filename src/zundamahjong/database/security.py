import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

from ..types.player import Player
from . import db
from .models import User
from .users import get_user, try_get_user

max_users = 256


class UserLimitException(Exception):
    """Thrown when the limit on the number of registered users is reached."""


class WrongPasswordException(Exception):
    """Thrown when the client types in an incorrect password."""


def login(name: str, password: str) -> Player:
    """Verify password and log in/register a user.

    - If an account with username :py:obj:`name` already exists, check the
      given password and log in.

    - If no such account exists *and* a password is given, create a new user
      account.

    - If no such account exists but no password is given, log the client
      into a temporary account.

    :returns: a :py:obj:`.Player` object with information for later use.
    :raises: :py:exc:`.UserLimitException`, :py:exc:`.WrongPasswordException`.
    """

    with db.session.begin():
        user = try_get_user(name)

        if user:
            if not check_password_hash(user.password, password):
                raise WrongPasswordException()

            else:
                return Player(name=name, has_account=True)

        elif password:
            num_users = db.session.scalar(sa.select(sa.func.count(User.id)))

            if num_users and num_users >= max_users:
                raise UserLimitException

            else:
                db.session.add(
                    User(name=name, password=generate_password_hash(password))
                )

                return Player(name=name, has_account=True, new_user=True)

        return Player(name=name)


def change_password(player: Player, cur_password: str, new_password: str) -> None:
    """Change the given player's login password.

    :param player: :py:class:`Player` object whose associated account we want
                   to change the password of. If no such account exists in the
                   database :py:func:`change_password` throws an exception.

    :param cur_password: Current password, meant to be input by the user.
    :param new_password: New password to hash and put in the database.

    :raises: :py:exc:`.WrongPasswordException`
    """

    with db.session.begin():
        user = get_user(player.name)

        if not check_password_hash(user.password, cur_password):
            raise WrongPasswordException("Current password is incorrect!")

        else:
            user.password = generate_password_hash(new_password)
