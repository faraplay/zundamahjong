# pyright: reportAny=false

import argparse
from importlib.metadata import version
import os

from werkzeug import run_simple
from werkzeug.serving import is_running_from_reloader

from .server import app


parser = argparse.ArgumentParser(
    prog="zundamahjong", description="Web-based Mahjong game server"
)

parser.add_argument("-p", "--port", type=int, help="port on which to listen")

parser.add_argument(
    "--debug", action="store_true", help="run server in development mode"
)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.port is None:
        port = int(os.getenv("DEBUG_SERVER_PORT", 5000))

    else:
        port = args.port

    if not is_running_from_reloader():
        print(f"Starting Zundamahjong server version {version('zundamahjong')}.")
        print(f"Go to http://localhost:{port} to play some Mahjong.")

    run_simple("localhost", port, app, threaded=True, use_reloader=args.debug)
