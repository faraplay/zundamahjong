import os

from flask import Flask, redirect, request, session, url_for
from werkzeug.wrappers import Response

from ..database import db
from ..database.security import login

app = Flask("zundamahjong", static_url_path="/zundamahjong/", static_folder="client")

secret_key = os.getenv("FLASK_SECRET_KEY")

if secret_key is None:
    print("Please set an actual secret key!")
    app.config["SECRET_KEY"] = "dev"

else:
    app.config["SECRET_KEY"] = secret_key

db.init_app(app)


@app.route("/")
def base() -> Response:
    return redirect(url_for("index"))


@app.route("/zundamahjong/")
def index() -> Response:
    if "player" not in session:
        return redirect(url_for("login_route"))

    return app.send_static_file("index.html")


@app.route("/zundamahjong/login/", methods=["GET", "POST"])
def login_route() -> Response:
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if name is None or password is None:
            raise RuntimeError

        player = login(name, password)
        session.clear()

        session["player"] = player.model_dump_json()

    if "player" in session:
        return redirect(url_for("index"))

    return app.send_static_file("login/index.html")
