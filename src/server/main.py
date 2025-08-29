from flask import Flask, request
from markupsafe import escape
from flask_socketio import SocketIO, emit
from pydantic import ValidationError


from ..mahjong.game import Game
from ..mahjong.action import Action

app = Flask(__name__)
socketio = SocketIO(app)

game = Game()

sid_players: dict[str, int] = {}
submitted_actions = [None, None, None, None]


def reset_submitted_actions():
    allowed_actions = [game.allowed_actions(player) for player in range(4)]
    submitted_actions[:] = [
        actions.default if len(actions.actions) == 1 else None
        for actions in allowed_actions
    ]
    if all(action is not None for action in submitted_actions):
        resolve_actions()
        reset_submitted_actions()


def resolve_actions():
    player, action = game.get_priority_action(submitted_actions)
    game.do_action(player, action)
    game.display_info()


def try_execute_actions():
    if any(action is None for action in submitted_actions):
        return
    resolve_actions()
    reset_submitted_actions()
    for sid, player in sid_players.items():
        emit("all_info", get_info(player), to=sid)


def get_info(player: int):
    return {
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
        "action_selected": submitted_actions[player] is not None,
    }


@socketio.on("connect")
def connect(auth):
    print(f"Client connected: {request.sid},\nAuth: {auth}")


@socketio.on("disconnect")
def disconnect(reason):
    print(f"Client disconnected: {request.sid},\nReason: {reason}")
    del sid_players[request.sid]


@socketio.on("set_player")
def handle_set_player(data):
    print(f"Received set_player from {request.sid}: {data}")
    try:
        player = int(data)
        if player not in range(4):
            print("Invalid player number!", player)
            return
    except ValueError:
        print("Received data is not an integer!", data)
        return
    sid_players[request.sid] = player
    emit("all_info", get_info(player))


@socketio.on("action")
def handle_action(data):
    print(f"Received action from {request.sid}: {data}")
    try:
        player = sid_players[request.sid]
    except KeyError:
        print(f"sid {request.sid} does not have an associated player!")
        return
    try:
        action = Action.model_validate(data)
    except ValidationError:
        print(f"Data could not be converted into Action object!")
    submitted_actions[player] = action
    print(submitted_actions)
    emit("action_received")
    try_execute_actions()


def run_server():
    reset_submitted_actions()
    socketio.run(app, debug=True)
