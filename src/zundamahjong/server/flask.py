import os

from flask import Flask, redirect, request, session, url_for
from werkzeug.serving import is_running_from_reloader
from werkzeug.wrappers import Response

from ..database import db
from ..database.security import WrongPasswordException, login

app = Flask("zundamahjong", static_url_path="/", static_folder="client")

secret_key = os.getenv("FLASK_SECRET_KEY")

NO_SECRET_KEY_ERROR_MESSAGE = """\
*********************************************************
FLASK_SECRET_KEY not found in the process environment!
Please generate a secure secret key for signing sessions.
Using an unsafe value from here on out.
*********************************************************
"""

if secret_key is None:
    if not is_running_from_reloader():
        print(NO_SECRET_KEY_ERROR_MESSAGE)
    app.config["SECRET_KEY"] = "dev"

else:
    app.config["SECRET_KEY"] = secret_key

db.init_app(app)


@app.route("/")
def index() -> Response:
    if "player" not in session:
        return redirect(url_for("login_route"))

    return app.send_static_file("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login_route() -> Response:
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if name is None or password is None:
            raise RuntimeError

        try:
            player = login(name, password)

        except WrongPasswordException:
            return redirect(url_for("login_route"))

        session.clear()

        session["player"] = player.model_dump_json()

    if "player" in session:
        return redirect(url_for("index"))

    return app.send_static_file("login/index.html")


@app.route("/logout/")
def logout_route() -> Response:
    session.clear()
    return redirect(url_for("login_route"))
