from flask import Flask, request
from markupsafe import escape
from flask_socketio import SocketIO, emit
from pydantic import ValidationError


from ..mahjong.action import Action
from ..mahjong.round import Round, RoundStatus
from ..mahjong.game import Game, GameOptions

app = Flask(__name__)
socketio = SocketIO(app)

game = Game(options=GameOptions(player_count=3))

sid_players: dict[str, int] = {}
submitted_actions = []


def resolve_action():
    player, action = game.round.get_priority_action(
        [submitted_actions[player] for player in range(game.player_count)]
    )
    game.round.do_action(player, action)
    game.round.display_info()


def set_default_submitted_actions():
    if game.round.status == RoundStatus.END:
        submitted_actions[:] = [None] * game.player_count
    else:
        allowed_actions = [
            game.round.allowed_actions(player) for player in range(game.player_count)
        ]
        submitted_actions[:] = [
            actions.default if len(actions.actions) == 1 else None
            for actions in allowed_actions
        ]


def try_resolve_actions():
    action_resolve_count = 0
    while all(action is not None for action in submitted_actions):
        resolve_action()
        action_resolve_count += 1
        set_default_submitted_actions()
    if action_resolve_count > 0:
        emit_info_all()


def get_win_info():
    return (
        None
        if game.win is None
        else {
            "player_scores": game.player_scores,
            "win": game.win.model_dump(),
            "scoring": game.scoring.model_dump(),
        }
    )


def get_round_info(player: int):
    hand = list(game.round.get_hand(player))
    history = [
        {"player": action[0], "action": action[1].model_dump()}
        for action in game.round.history
    ]
    discards = [discard.model_dump() for discard in game.round.discards]
    calls = [
        [call.model_dump() for call in game.round.get_calls(player)]
        for player in range(game.player_count)
    ]
    if game.round.status == RoundStatus.END:
        actions = None
    else:
        actions = [
            action.model_dump() for action in game.round.allowed_actions(player).actions
        ]
    action_selected = submitted_actions[player] is not None
    return {
        "player_count": game.player_count,
        "player": player,
        "wind_round": game.wind_round,
        "sub_round": game.sub_round,
        "player_scores": game.player_scores,
        "tiles_left": game.round.tiles_left,
        "current_player": game.round.current_player,
        "status": game.round.status.value,
        "hand": hand,
        "history": history,
        "discards": discards,
        "calls": calls,
        "actions": actions,
        "action_selected": action_selected,
    }


def emit_info(sid: str, player: int):
    emit(
        "info",
        {"round_info": get_round_info(player), "win_info": get_win_info()},
        to=sid,
    )


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


@socketio.on("next_round")
def start_next_round():
    if not game.can_start_next_round:
        print("Cannot start next round!")
        return
    print("Starting next round...")
    game.start_next_round()
    set_default_submitted_actions()
    game.round.display_info()
    emit_info_all()


@socketio.on("new_game")
def start_new_game():
    global game
    if not game.is_game_end:
        print("Game is still in progress!")
        return
    game = Game()
    game.round.display_info()
    emit_info_all()


@socketio.on("set_player")
def handle_set_player(data):
    print(f"Received set_player from {request.sid}: {data}")
    try:
        player = int(data)
        if player not in range(game.player_count):
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
    try_resolve_actions()


def run_server():
    set_default_submitted_actions()
    game.round.display_info()
    socketio.run(app, debug=True)
