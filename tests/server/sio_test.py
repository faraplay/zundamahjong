from flask import session
from flask.testing import FlaskClient
from flask_socketio import SocketIOTestClient

from zundamahjong.server import app
from zundamahjong.server.name_sid import sid_to_player
from zundamahjong.server.sio import sio
from zundamahjong.types.player import Player

from .conftest import AuthActions


def test_guest_login(client: FlaskClient, auth: AuthActions) -> None:
    with client:
        auth.login("test", "")
        session_player = Player.model_validate_json(session["player"])  # pyright: ignore[reportAny]
    assert session_player.name == "test"
    assert not session_player.has_account


def test_sio_connect(client: FlaskClient, auth: AuthActions) -> None:
    with client:
        auth.login("test", "")
        _ = SocketIOTestClient(app, sio, flask_test_client=client)
    assert len(sid_to_player) == 1
