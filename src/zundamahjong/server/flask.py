import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue
from werkzeug.serving import is_running_from_reloader

from ..database import db
from ..database.security import WrongPasswordException, login
from ..templates import imported_chunks, vite_manifest


app = Flask("zundamahjong", static_folder="client", static_url_path="/")
"""To-Do"""


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


# Other app housekeeping steps.
app.add_template_global(imported_chunks)
db.init_app(app)


@app.route("/")
def index() -> ResponseReturnValue:
    if "player" not in session:
        return redirect(url_for("login_route"))

    return render_template(
        "base.html",
        manifest=vite_manifest,
        name="src/main.tsx",
    )


@app.route("/login/", methods=["GET", "POST"])
def login_route() -> ResponseReturnValue:
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if name is None or password is None:
            raise RuntimeError

        try:
            player = login(name, password)

        except WrongPasswordException:
            flash("Incorrect password!")

        else:
            session.clear()
            session["player"] = player.model_dump_json()

    if "player" in session:
        return redirect(url_for("index"))

    return render_template(
        "base.html",
        manifest=vite_manifest,
        name="src/login.tsx",
    )


@app.route("/logout/")
def logout_route() -> ResponseReturnValue:
    session.clear()
    return redirect(url_for("login_route"))
