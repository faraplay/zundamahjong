from src.mahjong.action import Action
from src.mahjong.game_options import GameOptions

from .sio import sio, sio_on
from .name_sid import verify_name, get_player, set_player, remove_sid
from .player_info import Player
from .game_room import GameRoom


@sio_on("connect")
def connect(sid, environ, auth=None):
    pass


@sio_on("disconnect")
def disconnect(sid, reason):
    remove_sid(sid)


@sio_on("action")
def handle_action(sid, player_data, action_data):
    player = Player.model_validate(player_data)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        raise Exception("Player is not in a game room!")
    if game_room.game_controller is None:
        raise Exception("Game room has no active game!")
    action = Action.model_validate(action_data)
    game_room.game_controller.submit_action(player, action)


@sio_on("next_round")
def start_next_round(sid, player_data):
    player = Player.model_validate(player_data)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        raise Exception("Player is not in a game room!")
    if game_room.game_controller is None:
        raise Exception("Game room has no active game!")
    if not game_room.game_controller._game.is_game_end:
        game_room.game_controller.start_next_round(player)
    else:
        game_room.end_game()


@sio_on("set_name")
def on_set_name(sid, name):
    verify_name(name)
    player = Player.from_name(name)
    set_player(sid, player)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        return player.model_dump(), None, None
    game_room.rejoin(sid)
    if game_room.game_controller is None:
        return player.model_dump(), game_room.room_info, None
    game_room.game_controller.emit_info(player)
    return player.model_dump(), game_room.room_info, True


@sio_on("get_rooms")
def on_get_rooms(sid):
    return [game_room.room_info for game_room in GameRoom.get_rooms()]


@sio_on("create_room")
def on_create_room(sid, room_name, player_count):
    GameRoom.verify_player_count(player_count)
    GameRoom.verify_room_name(room_name)
    player = get_player(sid)
    return GameRoom.create_room(sid, player, room_name, player_count).room_info


@sio_on("join_room")
def on_join_room(sid, room_name):
    GameRoom.verify_room_name(room_name)
    player = get_player(sid)
    return GameRoom.join_room(sid, player, room_name).room_info


@sio_on("leave_room")
def on_leave_room(sid):
    player = get_player(sid)
    return GameRoom.leave_room(sid, player).room_info


@sio_on("start_game")
def on_start_game(sid, room_name, form_data):
    player = get_player(sid)
    game_room = GameRoom.get_player_room(player)
    if game_room is None or room_name != game_room.room_name:
        raise Exception(f"Player is not in room {room_name}!")
    game_options = GameOptions(
        player_count=form_data["player_count"],
        game_length=(
            form_data["game_length_wind_rounds"],
            form_data["game_length_sub_rounds"],
        ),
    )
    game_room.start_game(game_options)
