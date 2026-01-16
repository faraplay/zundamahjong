# pyright: reportIgnoreCommentWithoutRule=false

from enum import Enum
from threading import Lock
from typing import final
from weakref import WeakKeyDictionary

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
class _PlayerSID:
    """Helper class to hold Socket.IO client <-> :py:class:`Player` state."""

    def __init__(self) -> None:
        self.sid_to_player: dict[str, Player] = {}
        self.id_to_sid: dict[str, str] = {}
        self.player_sid_lock = Lock()


class PlayerStore:
    """TODO"""

    def __init__(self) -> None:
        self._storage_facility: WeakKeyDictionary[Flask, _PlayerSID] = (
            WeakKeyDictionary()
        )

    def init_app(self, app: Flask) -> None:
        self._storage_facility[app] = _PlayerSID()

    @property
    def _player_store(self) -> _PlayerSID:
        """TODO"""

        app = current_app._get_current_object()  # type: ignore  # pyright: ignore

        if app not in self._storage_facility:
            raise RuntimeError(
                "Please call `name_sid.init_app()` before using `name_sid.sid_to_player`!"
            )

        return self._storage_facility[app]

    @property
    def sid_to_player(self) -> dict[str, Player]:
        return self._player_store.sid_to_player

    @property
    def id_to_sid(self) -> dict[str, str]:
        return self._player_store.id_to_sid

    @property
    def player_sid_lock(self) -> Lock:
        return self._player_store.player_sid_lock

    def verify_name(self, name: str) -> None:
        """
        Raise an exception if the name is empty or too long.

        :param name: The name to verify.
        """
        if len(name) > 20:
            raise Exception("Name is over 20 characters long!")
        if name == "":
            raise Exception("Name cannot be empty!")

    def check_player(self, player: Player | None = None) -> PlayerStatus:
        """Check if a player Id is already connected to the Socket.IO server.

        :param player: Optional :py:class:`Player` instance to check against.
                    If not given, grab the player in the client's session.
        """

        if player and player.id in self.id_to_sid:
            return PlayerStatus.OTHER_SESSION

        elif "player" not in session:
            return PlayerStatus.NO_PLAYER

        session_player = Player.model_validate_json(session["player"])  # pyright: ignore[reportAny]

        if session_player.id in self.id_to_sid:
            return PlayerStatus.SAME_SESSION

        return PlayerStatus.OK_PLAYER

    def get_player(self, sid: str) -> Player:
        """
        Get the :py:class:`Player` object corresponding to a
        Socket.IO session id.

        :param sid: The Socket.IO session id to look up.
        """
        player = self.sid_to_player.get(sid)
        if player is None:
            raise Exception("Client has no name set!")
        return player

    def try_get_player(self, sid: str) -> Player | None:
        """
        Get the :py:class:`Player` object corresponding to a
        Socket.IO session id, or ``None`` if the session id has no associated
        :py:classs:`Player`.

        :param sid: The Socket.IO session id to look up.
        """
        return self.sid_to_player.get(sid)

    def set_player(self, sid: str, player: Player) -> None:
        """
        Set the :py:class:`Player` of a Socket.IO session id.

        :param sid: The Socket.IO session id to set the player for.
        :param player: The :py:class:`Player` to set.
        """
        with self.player_sid_lock:
            if self.id_to_sid.get(player.id, sid) != sid:
                raise Exception(f"Id {player.id} is already in use!")
            old_player = self.sid_to_player.get(sid)
            if old_player:
                self.id_to_sid.pop(old_player.id)
                close_room(old_player.id)
            self.id_to_sid[player.id] = sid
            self.sid_to_player[sid] = player
            join_room(player.id)

    def unset_player(self, sid: str) -> None:
        """
        Remove the associated :py:class:`Player` from a Socket.IO session id.

        :param sid: The Socket.IO session id to remove the player for.
        """
        with self.player_sid_lock:
            player = self.sid_to_player.get(sid)
            if player:
                self.id_to_sid.pop(player.id)
                self.sid_to_player.pop(sid)
                close_room(player.id)


player_store = PlayerStore()
"""TODO"""
