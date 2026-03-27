import os
from typing import final

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from zundamahjong.server import app as flask_app


@pytest.fixture
def app() -> Flask:
    flask_app.testing = True
    os.environ["DB_FILE"] = ":memory:"
    return flask_app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@final
class AuthActions:
    def __init__(self, client: FlaskClient) -> None:
        self._client = client

    def login(self, username: str = "test", password: str = "") -> TestResponse:
        return self._client.post(
            "/login/", data={"name": username, "password": password}
        )

    def logout(self) -> TestResponse:
        return self._client.get("/logout/")


@pytest.fixture
def auth(client: FlaskClient) -> AuthActions:
    return AuthActions(client)
