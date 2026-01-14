import sqlalchemy as sa

from . import db
from .models import User


def get_user(name: str) -> User:
    """Search the database decisively for a user account with the given
    username.

    :returns: a :py:class:`.User` object holding the found account's details.
    :throws: an exception if no such account is found.
    """

    return db.session.execute(sa.select(User).where(User.name == name)).scalar_one()


def try_get_user(name: str) -> User | None:
    """Search the database with no hope for a user account with the given username.

    :returns: either a :py:class:`.User` object holding the found account's details,
    :returns: or :py:obj:`None` if no such account is found.
    """

    return db.session.execute(
        sa.select(User).where(User.name == name)
    ).scalar_one_or_none()
