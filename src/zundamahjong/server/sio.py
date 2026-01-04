# pyright: reportIgnoreCommentWithoutRule=false

import logging
from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from flask import request
from flask_socketio import SocketIO as _SocketIO
from typing_extensions import Concatenate, ParamSpec

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

P = ParamSpec("P")
T = TypeVar("T")
Handler = Callable[Concatenate[str, P], T | None]


def sio_on(event: str) -> Callable[[Handler[P, T]], Callable[P, T | None]]:
    def sio_on_decorator(
        handler: Handler[P, T],
    ) -> Callable[P, T | None]:
        @wraps(handler)
        def wrapped_handler(*args: P.args, **kwargs: P.kwargs) -> T | None:
            with app.app_context():
                sid: str = request.sid  # type: ignore  # pyright: ignore
                assert isinstance(sid, str)
                try:
                    logger.debug(
                        f"Received event {event} from {sid} with args {repr(args)}"
                    )
                    return_value = handler(sid, *args, **kwargs)
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
