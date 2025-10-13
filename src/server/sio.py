from collections.abc import Callable
import logging
from typing import Any, Optional

from socketio import Server

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sio = Server(
    logger=logger,  # pyright: ignore[reportArgumentType]
    async_mode="threading",
)

Handler = Callable[..., Optional[Any]]


def emit_error(message: str, sid: str) -> None:
    sio.emit("error", {"message": message, "severity": "ERROR"}, to=sid)


def emit_warning(message: str, sid: str) -> None:
    sio.emit("error", {"message": message, "severity": "WARNING"}, to=sid)


def emit_info(message: str, sid: str) -> None:
    sio.emit("error", {"message": message, "severity": "INFO"}, to=sid)


def sio_on(event: str) -> Callable[[Handler], Handler]:
    def sio_on_decorator(
        handler: Handler,
    ) -> Handler:
        def wrapped_handler(sid: str, *args: Any) -> Optional[Any]:
            try:
                logger.debug(
                    f"Received event {event} from {sid} with args {repr(args)}"
                )
                return_value = handler(sid, *args)
                logger.debug(
                    f"Handler for event {event} from {sid} returned {repr(return_value)}"
                )
                return return_value
            except Exception as e:
                logger.error(e)
                emit_error(str(e), sid)
            return None

        sio.on(event, wrapped_handler)
        return wrapped_handler

    return sio_on_decorator
