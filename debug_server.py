import os
from werkzeug import run_simple
from werkzeug.middleware.shared_data import SharedDataMiddleware
from src.server import app

if __name__ == "__main__":
    debug_path = "/zundamahjong"
    debug_port = int(os.getenv("DEBUG_SERVER_PORT", 5000))
    app = SharedDataMiddleware(
        app,
        {
            debug_path: os.path.join(os.path.dirname(__file__), "client_build/"),
            f"{debug_path}/": os.path.join(
                os.path.dirname(__file__), "client_build/index.html"
            ),
        },
    )
    run_simple("localhost", debug_port, app, use_reloader=True, threaded=True)
