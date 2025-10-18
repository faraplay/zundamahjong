from collections.abc import Callable
import logging
from typing_extensions import Concatenate, ParamSpec

from socketio import Server as _Server

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Server(_Server):  # type: ignore[misc]
    def emit_error(self, message: str, to: str) -> None:
        self.emit("server_message", {"message": message, "severity": "ERROR"}, to=to)

    def emit_warning(self, message: str, to: str) -> None:
        self.emit("server_message", {"message": message, "severity": "WARNING"}, to=to)

    def emit_info(self, message: str, to: str) -> None:
        self.emit("server_message", {"message": message, "severity": "INFO"}, to=to)


sio = Server(
    logger=logger,  # pyright: ignore[reportArgumentType]
    async_mode="threading",
)


P = ParamSpec("P")
Handler = Callable[Concatenate[str, P], None]


def sio_on(event: str) -> Callable[[Handler[P]], Handler[P]]:
    def sio_on_decorator(
        handler: Handler[P],
    ) -> Handler[P]:
        def wrapped_handler(sid: str, *args: P.args, **kwargs: P.kwargs) -> None:
            try:
                logger.debug(
                    f"Received event {event} from {sid} with args {repr(args)}"
                )
                return_value = handler(sid, *args, **kwargs)
                logger.debug(
                    f"Handler for event {event} from {sid} returned {repr(return_value)}"
                )
                return return_value
            except Exception as e:
                logger.exception(e)
                sio.emit_error(str(e), to=sid)
            return None

        sio.on(event, wrapped_handler)
        return wrapped_handler

    return sio_on_decorator
