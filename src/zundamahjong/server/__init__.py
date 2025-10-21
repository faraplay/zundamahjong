from . import main as main
from .logger import create_root_logger, create_server_logger
from .flask import app

create_root_logger()
create_server_logger(__name__)

__all__ = ["app"]
