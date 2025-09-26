from .logger import create_server_logger, create_root_logger

create_root_logger()
create_server_logger(__name__)

from .sio import app
from . import main
