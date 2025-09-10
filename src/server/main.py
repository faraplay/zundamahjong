from flask import request
from flask_socketio import send, join_room, leave_room, rooms

from src.mahjong.action import Action
from src.mahjong.game_options import GameOptions

from .socketio import socketio, app
from .name_sid import verify_name, get_name, set_name, remove_sid
from .player_info import PlayerInfo
from .game_controller import GameController
from .game_room import GameRoom

game_controller = GameController(
    ["player:0", "player:1", "player:2", "player:3"], GameOptions()
)


@socketio.on("connect")
def connect(auth):
    print(f"Client connected: {request.sid},\nAuth: {auth}")


@socketio.on("disconnect")
def disconnect(reason):
    print(f"Client disconnected: {request.sid},\nReason: {reason}")
    remove_sid(request.sid)


@socketio.on("set_player")
def handle_set_player(player_data):
    print(f"Received set_player from {request.sid}: {player_data}")
    player = int(player_data)
    client_rooms = rooms()
    print(client_rooms)
    for room_name in client_rooms:
        if room_name.startswith("player:"):
            leave_room(room_name)
    player_info = PlayerInfo(player_id=f"player:{player}", player=player)
    join_room(player_info.player_id)
    game_controller.emit_info(player_info)
    return player_info.model_dump()


@socketio.on("action")
def handle_action(player_info_data, action_data):
    print(f"Received action from {request.sid}: {player_info_data}, {action_data}")
    player_info = PlayerInfo.model_validate(player_info_data)
    action = Action.model_validate(action_data)
    game_controller.submit_action(player_info, action)


@socketio.on("next_round")
def start_next_round(player_info_data):
    player_info = PlayerInfo.model_validate(player_info_data)
    game_controller.start_next_round(player_info)


@socketio.on("set_name")
def on_set_name(name):
    verify_name(name)
    print(f"Received set_name from {request.sid}: {name}")
    set_name(request.sid, name)
    game_room = GameRoom.get_player_room(name)
    room_info = game_room.room_info if game_room is not None else None
    return name, room_info


@socketio.on("get_rooms")
def on_get_rooms():
    return [game_room.room_info for game_room in GameRoom.get_rooms()]


@socketio.on("create_room")
def on_create_room(room_name, player_count):
    GameRoom.verify_player_count(player_count)
    GameRoom.verify_room_name(room_name)
    print(f"Received create_room from {request.sid}: {room_name} {player_count}")
    player_name = get_name(request.sid)
    return GameRoom.create_room(player_name, room_name, player_count).room_info


@socketio.on("join_room")
def on_join_room(room_name):
    GameRoom.verify_room_name(room_name)
    print(f"Received join_room from {request.sid}: {room_name}")
    player_name = get_name(request.sid)
    return GameRoom.join_room(player_name, room_name).room_info


@socketio.on("leave_room")
def on_leave_room():
    print(f"Received leave_room from {request.sid}")
    player_name = get_name(request.sid)
    return GameRoom.leave_room(player_name).room_info


@socketio.on_error()
def error_handler(e):
    send(str(e))


def run_server():
    socketio.run(app, debug=True)
