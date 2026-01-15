import os
import unittest

from flask import session
from flask_socketio import SocketIOTestClient
from typing_extensions import override

from zundamahjong.server import app
from zundamahjong.server.name_sid import sid_to_player
from zundamahjong.server.sio import sio
from zundamahjong.types.player import Player


class SocketIOTest(unittest.TestCase):
    @override
    def setUp(self) -> None:
        os.environ["DB_FILE"] = ":memory:"
        app.testing = True

    def test_guest_login(self) -> None:
        with app.test_client() as ftc:
            ftc.post("/login/", data={"name": "test", "password": ""})
            session_player = Player.model_validate_json(session["player"])  # pyright: ignore[reportAny]
        self.assertEqual(session_player.name, "test")
        self.assertEqual(session_player.has_account, False)

    def test_sio_connect(self) -> None:
        with app.test_client() as ftc:
            ftc.post("/login/", data={"name": "test", "password": ""})
            _ = SocketIOTestClient(app, sio, flask_test_client=ftc)
        self.assertEqual(len(sid_to_player), 1)
