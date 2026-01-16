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

parser = argparse.ArgumentParser(
    prog="zundamahjong", description="Web-based Mahjong game server"
)

parser.add_argument(
    "-p", "--port", type=int, help="port on which to run the Zundamahjong web server"
)

dev_args = parser.add_argument_group("dev options")

dev_args.add_argument(
    "--debug", action="store_true", help="run Zundamahjong in development mode"
)

dev_args.add_argument(
    "--vite-port", type=int, help="port on which to run the Vite development server"
)


def main() -> None:
    from .server import create_app

    flask_app: Flask = create_app()
    """Underlying :py:class:`flask.Flask` application object."""

    app: Flask | ProxyMiddleware = flask_app
    """Object that we pass to :py:func:`werkzeug.run_simple`."""

    args = parser.parse_args()

    if args.port is None:
        port = int(os.getenv("FLASK_PORT", 5000))

    else:
        port = args.port

    if args.debug:
        flask_app.debug = True

        if args.vite_port is None:
            vite_port = int(os.getenv("VITE_PORT", 5173))

        else:
            vite_port = args.vite_port

        flask_app.config["VITE_PORT"] = vite_port

        if not is_running_from_reloader():
            try:
                conn = http.client.HTTPConnection(
                    "localhost",
                    vite_port,
                )
                conn.request(
                    "GET",
                    "/src/app.tsx",
                )
                res = conn.getresponse()

                if res.status != 200:
                    print(
                        f"[ERROR]: Port {vite_port} is in use but not by the Vite debug server!\n"
                        + "Use the `--vite-port` command-line switch to use another port."
                    )
                    exit(1)

            except ConnectionRefusedError:
                print(f"Starting Vite debug server listening on port {vite_port}...")
                Popen(
                    [
                        "npm",
                        "--prefix",
                        "client",
                        "run",
                        "dev",
                        "--",
                        "--port",
                        str(vite_port),
                    ],
                    stdout=DEVNULL,
                )

        app = ProxyMiddleware(
            flask_app,
            {
                "/node_modules": {"target": f"http://localhost:{vite_port}"},
                "/src/assets": {"target": f"http://localhost:{vite_port}"},
            },
        )

    if not is_running_from_reloader():
        print(f"Starting Zundamahjong server version {version('zundamahjong')}...")
        print(f"Go to http://localhost:{port} to play some Mahjong.")

    run_simple("localhost", port, app, threaded=True, use_reloader=args.debug)
