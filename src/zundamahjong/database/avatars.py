from socketio import Server

from ..types.avatar import Avatar
from ..types.player import Player
from . import get_db, get_user


def get_avatar(sio: Server, sid: str, player: Player) -> Avatar:
    if not player.has_account:
        return Avatar(0)

    db = get_db(sio, sid)
    return get_user(db, player.name).avatar


def save_avatar(sio: Server, sid: str, player: Player, avatar: Avatar) -> None:
    if not player.has_account:
        return

    db = get_db(sio, sid)
    user = get_user(db, player.name)

    user.avatar = avatar
    db.commit()
