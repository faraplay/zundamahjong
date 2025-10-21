from collections.abc import Callable
import logging
from typing import Any, Optional

from flask import request
from flask_socketio import SocketIO as _SocketIO

from .flask import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SocketIO(_SocketIO):  # type: ignore[misc]
    def emit_error(self, message: str, to: str) -> None:
        self.emit("server_message", {"message": message, "severity": "ERROR"}, to=to)

    def emit_warning(self, message: str, to: str) -> None:
        self.emit("server_message", {"message": message, "severity": "WARNING"}, to=to)

    def emit_info(self, message: str, to: str) -> None:
        self.emit("server_message", {"message": message, "severity": "INFO"}, to=to)


sio = SocketIO(app, logger=logger, async_mode="threading")

Handler = Callable[..., Optional[Any]]


def sio_on(event: str) -> Callable[[Handler], Handler]:
    def sio_on_decorator(
        handler: Handler,
    ) -> Handler:
        def wrapped_handler(*args: Any) -> Optional[Any]:
            sid: str = request.sid  # type: ignore
            try:
                logger.debug(
                    f"Received event {event} from {sid} with args {repr(args)}"
                )
                return_value = handler(sid, *args)
                logger.debug(
                    f"Handler for event {event} from {sid} returned {return_value}"
                )
                return return_value
            except Exception as e:
                sio.emit_error(str(e), to=sid)
                logger.exception(e)
            return None

        sio.on_event(event, wrapped_handler)  # pyright: ignore[reportArgumentType]
        return wrapped_handler

    return sio_on_decorator
