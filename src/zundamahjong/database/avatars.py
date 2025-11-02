from ..types.avatar import Avatar
from ..types.player import Player
from . import db
from .users import get_user


def get_avatar(player: Player) -> Avatar:
    if not player.has_account:
        return Avatar(0)

    with db.session.begin():
        return get_user(player.name).avatar


def save_avatar(player: Player, avatar: Avatar) -> None:
    if not player.has_account:
        return

    with db.session.begin():
        user = get_user(player.name)
        user.avatar = avatar
