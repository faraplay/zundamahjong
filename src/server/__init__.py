from socketio import WSGIApp  # type: ignore[import-untyped]

from . import main
from .logger import create_root_logger, create_server_logger
from .sio import sio

create_root_logger()
create_server_logger(__name__)

app = WSGIApp(sio)
