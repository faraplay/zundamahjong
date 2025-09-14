import logging

logging.basicConfig(filename="server.log", encoding="utf-8", level=logging.INFO)

from .sio import debug_app, app
from . import main
