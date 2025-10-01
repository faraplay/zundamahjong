from collections.abc import Callable
import logging
from typing import Any

from socketio import Server

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sio = Server(logger=logger, async_mode="threading")  # pyright: ignore[reportArgumentType]


def sio_on(event: str):
    def sio_on_decorator(handler: Callable[..., Any | None]):
        def wrapped_handler(sid: str, *args):
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
                sio.send(str(e), to=sid)

        sio.on(event, wrapped_handler)
        return wrapped_handler

    return sio_on_decorator
