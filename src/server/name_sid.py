from threading import Lock

from .sio import sio
from .player_info import Player

sid_to_player: dict[str, Player] = {}
id_to_sid: dict[str, str] = {}
player_sid_lock = Lock()


def verify_name(name: str):
    if not isinstance(name, str):
        raise Exception("Name is not a string!")
    if len(name) > 20:
        raise Exception("Name is over 20 characters long!")
    if name == "":
        raise Exception("Name cannot be empty!")


def get_player(sid: str):
    try:
        return sid_to_player[sid]
    except KeyError:
        raise Exception("Client has no name set!")


def set_player(sid: str, player: Player):
    with player_sid_lock:
        if id_to_sid.get(player.id, sid) != sid:
            raise Exception(f"Id {player.id} is already in use!")
        old_player = sid_to_player.get(sid, None)
        if old_player:
            id_to_sid.pop(old_player.id)
            sio.close_room(old_player.id)
        id_to_sid[player.id] = sid
        sid_to_player[sid] = player
        sio.enter_room(sid, player.id)


def remove_sid(sid: str):
    with player_sid_lock:
        player = sid_to_player.get(sid, None)
        if player:
            id_to_sid.pop(player.id)
            sid_to_player.pop(sid)
            sio.close_room(player.id)
