from . import main as main
from .flask import create_app
from .logger import create_root_logger, create_server_logger

create_root_logger()
create_server_logger(__name__)

__all__ = ["create_app"]
