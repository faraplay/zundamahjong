from ..types.avatar import Avatar
from ..types.player import Player
from . import db
from .users import get_user


def get_avatar(player: Player) -> Avatar:
    """Return a player's last-chosen :py:class:`.Avatar`, if available. Fall
    back to :py:obj:`Avatar(0)`.

    :param player: Player whose name is used to search for an avatar.

    """

    if not player.has_account:
        return Avatar(0)

    with db.session.begin():
        return get_user(player.name).avatar


def save_avatar(player: Player, avatar: Avatar) -> None:
    """Store a player's newly chosen :py:class:`.Avatar` value in the
    application database. If it so happens that :py:obj:`player` does not have
    a user account then this is a no-op.

    :param player: Player for whom to save the new :py:class:`.Avatar` value.

    :param avatar: Value of :py:class:`.Avatar` to store in the database.

    """

    if not player.has_account:
        return

    with db.session.begin():
        user = get_user(player.name)
        user.avatar = avatar
