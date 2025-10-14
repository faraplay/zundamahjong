import os
from werkzeug import run_simple
from zundamahjong.server import app

if __name__ == "__main__":
    debug_port = int(os.getenv("DEBUG_SERVER_PORT", 5000))
    run_simple("localhost", debug_port, app, use_reloader=True, threaded=True)
