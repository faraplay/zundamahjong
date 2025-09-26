from collections.abc import Callable
import logging

from socketio import Server, WSGIApp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sio = Server(logger=logger, async_mode="threading")


def sio_on(event: str):
    def sio_on_decorator(handler: Callable):
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


app = WSGIApp(sio)
