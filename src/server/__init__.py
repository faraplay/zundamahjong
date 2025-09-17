from .logger import create_server_logger, create_root_logger

create_root_logger()
create_server_logger(__name__)

from .sio import debug_app, app
from . import main
