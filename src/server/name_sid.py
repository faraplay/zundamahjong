from threading import Lock
from typing import Optional

from .player_info import Player
from .sio import sio

sid_to_player: dict[str, Player] = {}
id_to_sid: dict[str, str] = {}
player_sid_lock = Lock()


def verify_name(name: str) -> None:
    if len(name) > 20:
        raise Exception("Name is over 20 characters long!")
    if name == "":
        raise Exception("Name cannot be empty!")


def get_player(sid: str) -> Player:
    player = sid_to_player.get(sid)
    if player is None:
        raise Exception("Client has no name set!")
    return player


def try_get_player(sid: str) -> Optional[Player]:
    return sid_to_player.get(sid)


def set_player(sid: str, player: Player) -> None:
    with player_sid_lock:
        if id_to_sid.get(player.id, sid) != sid:
            raise Exception(f"Id {player.id} is already in use!")
        old_player = sid_to_player.get(sid)
        if old_player:
            id_to_sid.pop(old_player.id)
            sio.close_room(old_player.id)
        id_to_sid[player.id] = sid
        sid_to_player[sid] = player
        sio.enter_room(sid, player.id)


def unset_player(sid: str) -> None:
    with player_sid_lock:
        player = sid_to_player.get(sid)
        if player:
            id_to_sid.pop(player.id)
            sid_to_player.pop(sid)
            sio.close_room(player.id)
