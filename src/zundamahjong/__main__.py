# pyright: reportAny=false

import argparse
import http.client
import os
from importlib.metadata import version
from subprocess import DEVNULL, Popen

from flask import Flask
from werkzeug import run_simple
from werkzeug.middleware.http_proxy import ProxyMiddleware
from werkzeug.serving import is_running_from_reloader

from .server import app as flask_app

parser = argparse.ArgumentParser(
    prog="zundamahjong", description="Web-based Mahjong game server"
)

parser.add_argument("-p", "--port", type=int, help="port on which to listen")

parser.add_argument(
    "--debug", action="store_true", help="run server in development mode"
)

app: Flask | ProxyMiddleware = flask_app
"""Object which we eventually pass to :py:func:`werkzeug.run_simple`."""


if __name__ == "__main__":
    args = parser.parse_args()

    if args.port is None:
        port = int(os.getenv("DEBUG_SERVER_PORT", 5000))

    else:
        port = args.port

    if args.debug:
        flask_app.debug = True

        if not is_running_from_reloader():
            try:
                conn = http.client.HTTPConnection("localhost", 5173)
                conn.request("GET", "/")

            except ConnectionRefusedError:
                print("Starting Vite debug server listening on port 5173...")
                Popen(["npm", "--prefix", "client", "run", "dev"], stdout=DEVNULL)

        app = ProxyMiddleware(
            flask_app,
            {
                "/src/assets": {"target": "http://localhost:5173"},
            },
        )

    if not is_running_from_reloader():
        print(f"Starting Zundamahjong server version {version('zundamahjong')}...")
        print(f"Go to http://localhost:{port} to play some Mahjong.")

    run_simple("localhost", port, app, threaded=True, use_reloader=args.debug)
