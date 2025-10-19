from flask import Flask, redirect, url_for
from werkzeug.wrappers import Response

flask_app = Flask(
    "zundamahjong", static_url_path="/zundamahjong/", static_folder="client"
)


@flask_app.route("/")
def base() -> Response:
    return redirect(url_for("index"))


@flask_app.route("/zundamahjong/")
def index() -> Response:
    return flask_app.send_static_file("index.html")
