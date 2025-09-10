from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms

from ..mahjong.action import Action
from ..mahjong.game_options import GameOptions

from .player_info import PlayerInfo
from .game_controller import GameController

app = Flask(__name__, static_folder="../../static")
socketio = SocketIO(app)

game_controller = GameController(
    ["player:0", "player:1", "player:2", "player:3"], GameOptions()
)


@socketio.on("connect")
def connect(auth):
    print(f"Client connected: {request.sid},\nAuth: {auth}")


@socketio.on("disconnect")
def disconnect(reason):
    print(f"Client disconnected: {request.sid},\nReason: {reason}")


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


@socketio.on_error()
def handle_error(e):
    print(str(e))


def run_server():
    socketio.run(app, debug=True)
