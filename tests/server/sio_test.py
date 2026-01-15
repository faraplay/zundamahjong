import os
import unittest

from flask import session
from flask.testing import FlaskClient
from typing_extensions import override

from zundamahjong.server import app


class SocketIOTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.flask_client: FlaskClient
        super().__init__(methodName)

    @override
    def setUp(self) -> None:
        os.environ["DB_FILE"] = ":memory:"
        app.testing = True
        self.flask_client = app.test_client()
        self.flask_client.__enter__()

    def test_guest_login(self) -> None:
        self.flask_client.post(
            "/login/",
            data={
                "name": "test",
                "password": "",
            },
        )

        self.assertEqual(
            session["player"],
            '{"name":"test","has_account":false,"new_user":false,"id":"player:test"}',
        )
