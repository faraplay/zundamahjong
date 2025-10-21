from flask import Flask, redirect, url_for
from werkzeug.wrappers import Response

from ..database import db

app = Flask("zundamahjong", static_url_path="/zundamahjong/", static_folder="client")

db.init_app(app)


@app.route("/")
def base() -> Response:
    return redirect(url_for("index"))


@app.route("/zundamahjong/")
def index() -> Response:
    return app.send_static_file("index.html")
