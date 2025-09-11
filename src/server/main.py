from flask import request
from flask_socketio import send

from src.mahjong.action import Action

from .socketio import socketio, app
from .name_sid import verify_name, get_player, set_player, remove_sid
from .player_info import Player
from .game_room import GameRoom


@socketio.on("connect")
def connect(auth):
    print(f"Client connected: {request.sid},\nAuth: {auth}")


@socketio.on("disconnect")
def disconnect(reason):
    print(f"Client disconnected: {request.sid},\nReason: {reason}")
    remove_sid(request.sid)


@socketio.on("action")
def handle_action(player_data, action_data):
    print(f"Received action from {request.sid}: {player_data}, {action_data}")
    player = Player.model_validate(player_data)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        raise Exception("Player is not in a game room!")
    if game_room.game_controller is None:
        raise Exception("Game room has no active game!")
    action = Action.model_validate(action_data)
    game_room.game_controller.submit_action(player, action)


@socketio.on("next_round")
def start_next_round(player_data):
    player = Player.model_validate(player_data)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        raise Exception("Player is not in a game room!")
    if game_room.game_controller is None:
        raise Exception("Game room has no active game!")
    game_room.game_controller.start_next_round(player)


@socketio.on("set_name")
def on_set_name(name):
    verify_name(name)
    print(f"Received set_name from {request.sid}: {name}")
    player = Player.from_name(name)
    set_player(request.sid, player)
    game_room = GameRoom.get_player_room(player)
    if game_room is None:
        return player.model_dump(), None
    if game_room.game_controller is not None:
        game_room.game_controller.emit_info(player)
    return player.model_dump(), game_room.room_info


@socketio.on("get_rooms")
def on_get_rooms():
    return [game_room.room_info for game_room in GameRoom.get_rooms()]


@socketio.on("create_room")
def on_create_room(room_name, player_count):
    GameRoom.verify_player_count(player_count)
    GameRoom.verify_room_name(room_name)
    print(f"Received create_room from {request.sid}: {room_name} {player_count}")
    player = get_player(request.sid)
    return GameRoom.create_room(player, room_name, player_count).room_info


@socketio.on("join_room")
def on_join_room(room_name):
    GameRoom.verify_room_name(room_name)
    print(f"Received join_room from {request.sid}: {room_name}")
    player = get_player(request.sid)
    return GameRoom.join_room(player, room_name).room_info


@socketio.on("leave_room")
def on_leave_room():
    print(f"Received leave_room from {request.sid}")
    player = get_player(request.sid)
    return GameRoom.leave_room(player).room_info


@socketio.on("start_game")
def on_start_game(room_name):
    print(f"Received start_game from {request.sid}")
    player = get_player(request.sid)
    game_room = GameRoom.get_player_room(player)
    if game_room is None or room_name != game_room.room_name:
        raise Exception(f"Player is not in room {room_name}!")
    game_room.start_game()


@socketio.on_error()
def error_handler(e):
    send(str(e))


def run_server():
    socketio.run(app, debug=True)
