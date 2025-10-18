import logging
from typing import Any

from ..database.security import change_password, login
from ..mahjong.action import action_adapter
from ..mahjong.game_options import GameOptions
from ..types.avatar import Avatar

from .game_room import GameRoom
from .name_sid import get_player, set_player, try_get_player, unset_player, verify_name
from .sio import sio, sio_on

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sio_on("connect")
def connect(sid: str, environ: dict[str, Any], auth: object = None) -> None:  # pyright: ignore[reportExplicitAny]
    logger.info(f"Client connecting with sid {sid}")


@sio_on("disconnect")
def disconnect(sid: str, reason: str) -> None:
    logger.info(f"Client disconnecting with sid {sid}, reason {reason}")
    player = try_get_player(sid)
    if player is None:
        logger.info(f"Client {sid} had no set name")
    else:
        GameRoom.try_disconnect(player)
    unset_player(sid)


@sio_on("action")
def handle_action(sid: str, action_data: object, history_index: object) -> None:
    if not isinstance(history_index, int):
        raise Exception("Argument history_index is not an integer!")
    player = get_player(sid)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        raise Exception("Player is not in a game room!")
    if game_room.game_controller is None:
        raise Exception("Game room has no active game!")
    action = action_adapter.validate_python(action_data)
    game_room.game_controller.submit_action(player, action, history_index)


@sio_on("next_round")
def start_next_round(sid: str) -> None:
    player = get_player(sid)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        raise Exception("Player is not in a game room!")
    if game_room.game_controller is None:
        raise Exception("Game room has no active game!")
    if not game_room.game_controller.game.is_game_end:
        game_room.game_controller.start_next_round(player)
    else:
        game_room.end_game()


@sio_on("set_name")
def on_set_name(sid: str, name: object, password: object) -> None:
    if not isinstance(name, str):
        raise Exception("Argument name is not a string!")
    if not isinstance(password, str):
        raise Exception("Argument password is not a string!")
    verify_name(name)
    player = login(name, password)
    set_player(sid, player)
    if player.has_account and player.new_user:
        sio.emit_info("Account successfully created.", to=sid)
    sio.emit("player_info", player.model_dump(), to=sid)
    game_room = GameRoom.try_reconnect(player)
    if game_room is not None and game_room.game_controller is not None:
        game_room.game_controller.emit_info(player)


@sio_on("unset_name")
def on_unset_name(sid: str) -> None:
    GameRoom.try_disconnect(get_player(sid))
    unset_player(sid)
    sio.emit("unset_name", to=sid)


@sio_on("change_password")
def on_change_password(sid: str, cur_password: object, new_password: object) -> None:
    if not isinstance(cur_password, str):
        raise Exception("Argument cur_password is not a string!")
    if not isinstance(new_password, str):
        raise Exception("Argument new_password is not a string!")
    change_password(get_player(sid), cur_password, new_password)
    sio.emit_info("Password changed successfully.", to=sid)


@sio_on("get_rooms")
def on_get_rooms(sid: str) -> None:
    GameRoom.emit_rooms_list(sid)


@sio_on("create_room")
def on_create_room(sid: str, room_name: object, player_count: object) -> None:
    if not isinstance(room_name, str):
        raise Exception("Argument room_name is not a string!")
    if not isinstance(player_count, int):
        raise Exception("Argument player_count is not an int!")
    GameRoom.verify_player_count(player_count)
    GameRoom.verify_room_name(room_name)
    GameRoom.create_room(get_player(sid), room_name, player_count)


@sio_on("join_room")
def on_join_room(sid: str, room_name: object) -> None:
    if not isinstance(room_name, str):
        raise Exception("Argument room_name is not a string!")
    GameRoom.verify_room_name(room_name)
    GameRoom.join_room(get_player(sid), room_name)


@sio_on("leave_room")
def on_leave_room(sid: str) -> None:
    GameRoom.leave_room(get_player(sid))


@sio_on("set_avatar")
def on_set_avatar(sid: str, avatar_code: object) -> None:
    if not isinstance(avatar_code, int):
        raise Exception("Avatar code is not an integer!")
    avatar = Avatar(avatar_code)
    GameRoom.set_avatar(get_player(sid), avatar)


@sio_on("game_options")
def on_game_options(sid: str, game_options_data: object) -> None:
    game_options = GameOptions.model_validate(game_options_data)
    GameRoom.set_game_options(get_player(sid), game_options)


@sio_on("start_game")
def on_start_game(sid: str) -> None:
    game_room = GameRoom.get_player_room(get_player(sid))
    if game_room is None:
        raise Exception("Player is not in a room!")
    game_room.start_game()
