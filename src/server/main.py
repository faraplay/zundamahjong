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
    emit("list_all", list(game.history))


def run_server():
    socketio.run(app, debug=True)
