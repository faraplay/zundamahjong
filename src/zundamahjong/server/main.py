import logging
from typing import Any

from flask import session

from ..database.security import change_password
from ..mahjong.action import action_adapter
from ..mahjong.game_options import GameOptions
from ..types.avatar import Avatar
from ..types.player import Player
from .game_room import GameRoom
from .name_sid import get_player, set_player, try_get_player, unset_player
from .sio import sio, sio_on

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sio_on("connect")
def connect(sid: str, environ: dict[str, Any], auth: object = None) -> None:  # pyright: ignore[reportExplicitAny]
    """
    Handle a new Socket.IO connection.
    Note that the client should already have logged in through the Flask login route.

    Get player information from the Flask ``session`` object.
    Then set the player on the :py:mod:`name_sid` module and send the client their
    :py:class:`Player` object.
    If they are in an active game, make them rejoin the game.

    :param sid: The Socket.IO session id of the connection.
    """
    logger.info(f"Client connecting with sid {sid}")
    if "player" not in session:
        raise Exception("Player object missing from client session!")
    player = Player.model_validate_json(session["player"])  # pyright: ignore[reportAny]
    set_player(sid, player)
    if player.new_user and session["first"]:
        sio.emit_info("Account successfully created.", to=sid)
    sio.emit("player_info", player.model_dump(), to=sid)
    game_room = GameRoom.try_reconnect(player)
    if game_room is not None and game_room.game_controller is not None:
        game_room.game_controller.emit_info(player)


@sio_on("disconnect")
def disconnect(sid: str, reason: str) -> None:
    """
    Handle a Socket.IO disconnection.

    Disconnect the player from their game if they are in a game,
    and unset the player on the :py:mod:`name_sid` module.

    :param sid: The Socket.IO session id of the connection.
    """
    logger.info(f"Client disconnecting with sid {sid}, reason {reason}")
    player = try_get_player(sid)
    if player is None:
        logger.info(f"Client {sid} had no set name")
    else:
        GameRoom.try_disconnect(player)
    unset_player(sid)


@sio_on("change_password")
def on_change_password(sid: str, cur_password: object, new_password: object) -> None:
    """
    Change a player's password.

    :param sid: The Socket.IO session id of the connection.
    :param cur_password: The player's current password.
    :param new_password: The player's new password.
    """
    if not isinstance(cur_password, str):
        raise Exception("Argument cur_password is not a string!")
    if not isinstance(new_password, str):
        raise Exception("Argument new_password is not a string!")
    change_password(get_player(sid), cur_password, new_password)
    sio.emit_info("Password changed successfully.", to=sid)


@sio_on("get_rooms")
def on_get_rooms(sid: str) -> None:
    """
    Send the client a list of game rooms.

    :param sid: The Socket.IO session id of the connection.
    """
    GameRoom.emit_rooms_list(sid)


@sio_on("create_room")
def on_create_room(sid: str, room_name: object, player_count: object) -> None:
    """
    Create a new game room and add the creating player to it.

    :param sid: The Socket.IO session id of the connection.
    :param room_name: The name of the game room.
    :param player_count: The number of players the game room can hold.
    """
    if not isinstance(room_name, str):
        raise Exception("Argument room_name is not a string!")
    if not isinstance(player_count, int):
        raise Exception("Argument player_count is not an int!")
    GameRoom.verify_player_count(player_count)
    GameRoom.verify_room_name(room_name)
    GameRoom.create_room(get_player(sid), room_name, player_count)


@sio_on("join_room")
def on_join_room(sid: str, room_name: object) -> None:
    """
    Add a player to a game room.

    :param sid: The Socket.IO session id of the connection.
    :param room_name: The name of the game room.
    """
    if not isinstance(room_name, str):
        raise Exception("Argument room_name is not a string!")
    GameRoom.verify_room_name(room_name)
    GameRoom.join_room(get_player(sid), room_name)


@sio_on("leave_room")
def on_leave_room(sid: str) -> None:
    """
    Remove a player from the game room they are currently in.

    :param sid: The Socket.IO session id of the connection.
    """
    GameRoom.leave_room(get_player(sid))


@sio_on("set_avatar")
def on_set_avatar(sid: str, avatar_code: object) -> None:
    """
    Set a player's avatar. The player should be in a game room.

    :param sid: The Socket.IO session id of the connection.
    :param avatar_code: The code of the avatar.
    """
    if not isinstance(avatar_code, int):
        raise Exception("Avatar code is not an integer!")
    avatar = Avatar(avatar_code)
    GameRoom.set_avatar(get_player(sid), avatar)


@sio_on("game_options")
def on_game_options(sid: str, game_options_data: object) -> None:
    """
    Set the game options of the game room a player is in.

    :param sid: The Socket.IO session id of the connection.
    :param game_options_data: The game options JSON object.
    """
    game_options = GameOptions.model_validate(game_options_data)
    GameRoom.set_game_options(get_player(sid), game_options)


@sio_on("start_game")
def on_start_game(sid: str) -> None:
    """
    Start the game in the game room the player is in.

    :param sid: The Socket.IO session id of the connection.
    """
    game_room = GameRoom.get_player_room(get_player(sid))
    if game_room is None:
        raise Exception("Player is not in a room!")
    game_room.start_game()


@sio_on("action")
def handle_action(sid: str, action_data: object, history_index: object) -> None:
    """
    Submit a player's action to the game of the game room they are in.

    Check the player is in a game room with an active game.
    If so, submit the sent action to this game.

    :param sid: The Socket.IO session id of the connection.
    :param action_data: The :py:class:`Action` the player is submitting, as a
                            JSON object.
    :param history_index: The moment within the game when they are submitting
                          the action, measured in terms of number of actions
                          in the game's history.
    """
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
    """
    Start the next round of the game of the game room the player is in,
    or end the game if it is the end of the last round.

    Check the player is in a game room with an active game.
    If so, check whether the game has reached the end state of
    the last round. If so, end the game room's game.
    Otherwise, attempt to start the next round.

    :param sid: The Socket.IO session id of the connection.
    """
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
