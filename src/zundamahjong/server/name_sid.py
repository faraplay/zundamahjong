from threading import Lock

from flask_socketio import close_room, join_room

from ..types.player import Player

sid_to_player: dict[str, Player] = {}
id_to_sid: dict[str, str] = {}
player_sid_lock = Lock()


def verify_name(name: str) -> None:
    """
    Raise an exception if the name is empty or too long.

    :param name: The name to verify.
    """
    if len(name) > 20:
        raise Exception("Name is over 20 characters long!")
    if name == "":
        raise Exception("Name cannot be empty!")


def get_player(sid: str) -> Player:
    """
    Get the :py:class:`Player` object corresponding to a
    Socket.IO session id.

    :param sid: The Socket.IO session id to look up.
    """
    player = sid_to_player.get(sid)
    if player is None:
        raise Exception("Client has no name set!")
    return player


def try_get_player(sid: str) -> Player | None:
    """
    Get the :py:class:`Player` object corresponding to a
    Socket.IO session id, or ``None`` if the session id has no associated
    :py:classs:`Player`.

    :param sid: The Socket.IO session id to look up.
    """
    return sid_to_player.get(sid)


def set_player(sid: str, player: Player) -> None:
    """
    Set the :py:class:`Player` of a Socket.IO session id.

    :param sid: The Socket.IO session id to set the player for.
    :param player: The :py:class:`Player` to set.
    """
    with player_sid_lock:
        if id_to_sid.get(player.id, sid) != sid:
            raise Exception(f"Id {player.id} is already in use!")
        old_player = sid_to_player.get(sid)
        if old_player:
            id_to_sid.pop(old_player.id)
            close_room(old_player.id)
        id_to_sid[player.id] = sid
        sid_to_player[sid] = player
        join_room(player.id)


def unset_player(sid: str) -> None:
    """
    Remove the associated :py:class:`Player` from a Socket.IO session id.

    :param sid: The Socket.IO session id to remove the player for.
    """
    with player_sid_lock:
        player = sid_to_player.get(sid)
        if player:
            id_to_sid.pop(player.id)
            sid_to_player.pop(sid)
            close_room(player.id)
