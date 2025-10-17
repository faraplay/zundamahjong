from flask import Flask, redirect, url_for
from werkzeug.wrappers import Response

wsgi_app = Flask(
    "zundamahjong", static_url_path="/zundamahjong/", static_folder="client"
)


@wsgi_app.route("/")
def base() -> Response:
    return redirect(url_for("index"))


@wsgi_app.route("/zundamahjong/")
def index() -> Response:
    return wsgi_app.send_static_file("index.html")
