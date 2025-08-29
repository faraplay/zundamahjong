from flask import Flask, request
from markupsafe import escape
from flask_socketio import SocketIO, emit
from pydantic import ValidationError


from ..mahjong.game import Game, GameStatus
from ..mahjong.action import Action

app = Flask(__name__)
socketio = SocketIO(app)

game = Game()

sid_players: dict[str, int] = {}
submitted_actions = [None, None, None, None]


def reset_submitted_actions():
    if game.status == GameStatus.END:
        submitted_actions[:] = [None, None, None, None]
        return
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
    emit_info_all()


def get_win_info():
    if game.win_info is not None:
        return {
            "win_player": game.win_info.win_player,
            "hand": game.win_info.hand,
            "calls": [call.model_dump() for call in game.win_info.calls],
        }
    else:
        return None


def get_game_info(player: int):
    return {
        "player": player,
        "hand": list(game.get_hand(player)),
        "tiles_left": game.wall_count,
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


def emit_info(sid: str, player: int):
    if game.status != GameStatus.END:
        emit("game_info", get_game_info(player), to=sid)
    else:
        emit("win_info", get_win_info(), to=sid)


def emit_info_all():
    for sid, player in sid_players.items():
        emit_info(sid, player)


@socketio.on("connect")
def connect(auth):
    print(f"Client connected: {request.sid},\nAuth: {auth}")


@socketio.on("disconnect")
def disconnect(reason):
    print(f"Client disconnected: {request.sid},\nReason: {reason}")
    sid_players.pop(request.sid, None)


@socketio.on("new_game")
def start_new_game():
    print("Starting new game...")
    global game
    game = Game()
    emit_info_all()


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
    emit_info(request.sid, player)


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
    while game.wall_count > 20:
        actions = [game.allowed_actions(player).default for player in range(4)]
        player, action = game.get_priority_action(actions)
        game.do_action(player, action)
    reset_submitted_actions()
    socketio.run(app, debug=True)
