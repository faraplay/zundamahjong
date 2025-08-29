from flask import Flask, request
from markupsafe import escape
from flask_socketio import SocketIO, emit

from ..mahjong.game import Game

app = Flask(__name__)
socketio = SocketIO(app)

game = Game()


@socketio.on("connect")
def connect(auth):
    print(f"Client connected: {request.sid},\nAuth: {auth}")


@socketio.on("disconnect")
def disconnect(reason):
    print(f"Client disconnected: {request.sid},\nReason: {reason}")


@socketio.on("set_player")
def handle_set_player(data):
    print(f"Received message from {request.sid}: {data}")
    try:
        player = int(data)
        if player not in range(4):
            print("Invalid player number!", player)
            return
    except ValueError:
        print("Received data is not an integer!", data)
        return
    info = {
        "player": player,
        "hand": list(game.get_hand(player)),
        "history": [
            {"player": action[0], "action": action[1].model_dump()}
            for action in game.history
        ],
        "discards": list(game.discard_pool),
        "player_calls": [
            {
                "player": player,
                "calls": [call.model_dump() for call in game.get_calls(player)],
            }
            for player in range(4)
        ],
        "actions": [
            action.model_dump() for action in game.allowed_actions(player).actions
        ],
    }
    emit("all_info", info)


def run_server():
    socketio.run(app, debug=True)
