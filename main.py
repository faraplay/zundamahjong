from werkzeug import run_simple
from src.server import debug_app

if __name__ == "__main__":
    run_simple("localhost", 5000, debug_app, use_reloader=True, threaded=True)
