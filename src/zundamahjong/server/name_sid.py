import random
from enum import Enum
from threading import Lock
from typing import final

from flask import Flask, current_app, session
from flask_socketio import close_room, join_room

from ..types.player import Player


class PlayerStatus(Enum):
    NO_PLAYER = 0
    """No player stored in browser session"""

    OK_PLAYER = 1
    """All OK to start Socket.IO connection"""

    OTHER_SESSION = -1
    """Player Id in use from another device"""

    SAME_SESSION = -2
    """Player Id in use from same device!"""


@final
class PlayerStore:
    """Helper class to hold Socket.IO client <-> :py:class:`Player` state."""

    def __init__(self) -> None:
        self.sid_to_player: dict[str, Player] = {}
        self.id_to_sid: dict[str, str] = {}
        self.player_sid_lock = Lock()


class NameSID:
    """Wrapper around :py:class:`PlayerStore`, built as a Flask extension."""

    def __init__(self) -> None:
        self._storage_facility: dict[str, PlayerStore] = {}

    def init_app(self, app: Flask) -> None:
        key = f"{random.getrandbits(64):016x}"
        app.extensions["name_sid_key"] = key

        self._storage_facility[key] = PlayerStore()

    @property
    def current_pstore(self) -> PlayerStore:
        try:
            key = current_app.extensions["name_sid_key"]  # pyright: ignore[reportAny]
            assert isinstance(key, str)
        except KeyError:
            raise RuntimeError("TODO")

        return self._storage_facility[key]

    @property
    def sid_to_player(self) -> dict[str, Player]:
        return self.current_pstore.sid_to_player

    @property
    def id_to_sid(self) -> dict[str, str]:
        return self.current_pstore.id_to_sid

    @property
    def player_sid_lock(self) -> Lock:
        return self.current_pstore.player_sid_lock


name_sid = NameSID()
"""TODO"""


def verify_name(name: str) -> None:
    """
    Raise an exception if the name is empty or too long.

    :param name: The name to verify.
    """
    if len(name) > 20:
        raise Exception("Name is over 20 characters long!")
    if name == "":
        raise Exception("Name cannot be empty!")


def check_player(player: Player | None = None) -> PlayerStatus:
    """Check if a player Id is already connected to the Socket.IO server.

    :param player: Optional :py:class:`Player` instance to check against.
                   If not given, grab the player in the client's session.
    """

    if player and player.id in name_sid.id_to_sid:
        return PlayerStatus.OTHER_SESSION

    elif "player" not in session:
        return PlayerStatus.NO_PLAYER

    session_player = Player.model_validate_json(session["player"])  # pyright: ignore[reportAny]

    if session_player.id in name_sid.id_to_sid:
        return PlayerStatus.SAME_SESSION

    return PlayerStatus.OK_PLAYER


def get_player(sid: str) -> Player:
    """
    Get the :py:class:`Player` object corresponding to a
    Socket.IO session id.

    :param sid: The Socket.IO session id to look up.
    """
    player = name_sid.sid_to_player.get(sid)
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
    return name_sid.sid_to_player.get(sid)


def set_player(sid: str, player: Player) -> None:
    """
    Set the :py:class:`Player` of a Socket.IO session id.

    :param sid: The Socket.IO session id to set the player for.
    :param player: The :py:class:`Player` to set.
    """
    with name_sid.player_sid_lock:
        if name_sid.id_to_sid.get(player.id, sid) != sid:
            raise Exception(f"Id {player.id} is already in use!")
        old_player = name_sid.sid_to_player.get(sid)
        if old_player:
            name_sid.id_to_sid.pop(old_player.id)
            close_room(old_player.id)
        name_sid.id_to_sid[player.id] = sid
        name_sid.sid_to_player[sid] = player
        join_room(player.id)


def unset_player(sid: str) -> None:
    """
    Remove the associated :py:class:`Player` from a Socket.IO session id.

    :param sid: The Socket.IO session id to remove the player for.
    """
    with name_sid.player_sid_lock:
        player = name_sid.sid_to_player.get(sid)
        if player:
            name_sid.id_to_sid.pop(player.id)
            name_sid.sid_to_player.pop(sid)
            close_room(player.id)
