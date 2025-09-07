from flask import Flask, request
from markupsafe import escape
from flask_socketio import SocketIO, emit
from pydantic import ValidationError


from ..mahjong.round import Round, RoundStatus
from ..mahjong.action import Action

app = Flask(__name__)
socketio = SocketIO(app)

round = Round()

sid_seats: dict[str, int] = {}
submitted_actions = [None, None, None, None]


def reset_submitted_actions():
    if round.status == RoundStatus.END:
        submitted_actions[:] = [None, None, None, None]
        return
    allowed_actions = [round.allowed_actions(seat) for seat in range(4)]
    submitted_actions[:] = [
        actions.default if len(actions.actions) == 1 else None
        for actions in allowed_actions
    ]
    if all(action is not None for action in submitted_actions):
        resolve_actions()
        reset_submitted_actions()


def resolve_actions():
    seat, action = round.get_priority_action(submitted_actions)
    round.do_action(seat, action)
    round.display_info()


def try_execute_actions():
    if any(action is None for action in submitted_actions):
        return
    resolve_actions()
    reset_submitted_actions()
    emit_info_all()


def get_win_info():
    if round.win_info is not None:
        return {
            "win_seat": round.win_info.win_seat,
            "hand": round.win_info.hand,
            "calls": [call.model_dump() for call in round.win_info.calls],
        }
    else:
        return None


def get_round_info(seat: int):
    return {
        "player": seat,
        "seat": seat,
        "wind_round": 0,
        "seat_round": 0,
        "tiles_left": round.tiles_left,
        "player_scores": [100, 200, 300, -600],
        "current_seat": round.current_seat,
        "status": round.status.value,
        "hand": list(round.get_hand(seat)),
        "history": [
            {"seat": action[0], "action": action[1].model_dump()}
            for action in round.history
        ],
        "discards": [discard.model_dump() for discard in round.discards],
        "calls": [
            [call.model_dump() for call in round.get_calls(seat)] for seat in range(4)
        ],
        "actions": [
            action.model_dump() for action in round.allowed_actions(seat).actions
        ],
        "action_selected": submitted_actions[seat] is not None,
    }


def emit_info(sid: str, seat: int):
    if round.status != RoundStatus.END:
        emit("round_info", get_round_info(seat), to=sid)
    else:
        emit("win_info", get_win_info(), to=sid)


def emit_info_all():
    for sid, seat in sid_seats.items():
        emit_info(sid, seat)


@socketio.on("connect")
def connect(auth):
    print(f"Client connected: {request.sid},\nAuth: {auth}")


@socketio.on("disconnect")
def disconnect(reason):
    print(f"Client disconnected: {request.sid},\nReason: {reason}")
    sid_seats.pop(request.sid, None)


@socketio.on("new_round")
def start_new_round():
    print("Starting new round...")
    global round
    round = Round()
    reset_submitted_actions()
    emit_info_all()


@socketio.on("set_seat")
def handle_set_seat(data):
    print(f"Received set_seat from {request.sid}: {data}")
    try:
        seat = int(data)
        if seat not in range(4):
            print("Invalid seat number!", seat)
            return
    except ValueError:
        print("Received data is not an integer!", data)
        return
    sid_seats[request.sid] = seat
    emit_info(request.sid, seat)


@socketio.on("action")
def handle_action(data):
    print(f"Received action from {request.sid}: {data}")
    try:
        seat = sid_seats[request.sid]
    except KeyError:
        print(f"sid {request.sid} does not have an associated seat!")
        return
    try:
        action = Action.model_validate(data)
    except ValidationError:
        print(f"Data could not be converted into Action object!")
    submitted_actions[seat] = action
    print(submitted_actions)
    emit("action_received")
    try_execute_actions()


def run_server():
    reset_submitted_actions()
    socketio.run(app, debug=True)
