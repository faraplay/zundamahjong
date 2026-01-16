from enum import Enum

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue
from werkzeug.serving import is_running_from_reloader

from ..database import db
from ..database.security import UserLimitException, WrongPasswordException, login
from ..templates import manifest
from ..types.player import Player
from .name_sid import id_to_sid
from .sio import sio

BAD_SECRET_KEY_ERROR_MESSAGE = """\
*********************************************************
Unsafe FLASK_SECRET_KEY found in process environment!
Please generate a secure secret key for signing sessions.
*********************************************************
"""


def create_app(test_config: dict[str, str | bool | None] | None = None) -> Flask:
    """Flask application factory."""

    app = Flask(
        "zundamahjong",
        static_url_path="/",
        static_folder="client",
    )

    app.config.from_mapping(
        {
            "SECRET_KEY": "dev",
        }
    )

    app.config.from_prefixed_env()

    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)
    manifest.init_app(app)
    sio.init_app(app)

    if app.config["SECRET_KEY"] == "dev" and not is_running_from_reloader():
        print(BAD_SECRET_KEY_ERROR_MESSAGE)

    @app.route("/")
    def index() -> ResponseReturnValue:
        """Main route where a Socket.IO connection is established."""

        if check_player() != PlayerStatus.OK_PLAYER:
            return redirect(url_for("login_route"))

        session["first"] = False if "first" in session else True

        return render_template("index.html")

    @app.route("/login/", methods=["GET", "POST"])
    def login_route() -> ResponseReturnValue:
        """Page users go through to set their name/login to their account.

        If there is a valid player Id stored in the client's session, send
        client to the main :py:mod:`zundamahjong` page where a Socket.IO connection
        is established.

        Under a `POST` request, validate user input and try to log in. If not
        in use elsewhere, store resulting player Id to the client session.
        """

        status = check_player()

        if status == PlayerStatus.OK_PLAYER:
            return redirect(url_for("index"))

        elif status == PlayerStatus.SAME_SESSION:
            flash("You are logged in on another tab!")

        elif request.method == "POST":
            try:
                player = login(
                    request.form["name"],
                    request.form["password"],
                )

            except UserLimitException:
                flash("Unable to create new user accounts!")

            except WrongPasswordException:
                flash("Incorrect password!")

            else:
                if check_player(player) == PlayerStatus.OTHER_SESSION:
                    flash("You are logged in on another device!")

                else:
                    session.clear()
                    session["player"] = player.model_dump_json()
                    return redirect(url_for("index"))

        return render_template("login.html")

    @app.route("/logout/")
    def logout_route() -> ResponseReturnValue:
        session.clear()
        return redirect(url_for("login_route"))

    return app


class PlayerStatus(Enum):
    NO_PLAYER = 0
    """No player stored in browser session"""

    OK_PLAYER = 1
    """All OK to start Socket.IO connection"""

    OTHER_SESSION = -1
    """Player Id in use from another device"""

    SAME_SESSION = -2
    """Player Id in use from same device!"""


def check_player(player: Player | None = None) -> PlayerStatus:
    """Check if a player Id is already connected to the Socket.IO server.

    :param player: Optional :py:class:`Player` instance to check against.
                   If not given, grab the player in the client's session.
    """

    if player and player.id in id_to_sid:
        return PlayerStatus.OTHER_SESSION

    elif "player" not in session:
        return PlayerStatus.NO_PLAYER

    session_player = Player.model_validate_json(session["player"])  # pyright: ignore[reportAny]

    if session_player.id in id_to_sid:
        return PlayerStatus.SAME_SESSION

    return PlayerStatus.OK_PLAYER
