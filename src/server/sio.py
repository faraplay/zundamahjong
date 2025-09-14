from collections.abc import Callable
import logging

from socketio import Server, WSGIApp

logger = logging.getLogger(__name__)

sio = Server(logger=logger, async_mode="threading")


def sio_on(event: str):
    def sio_on_decorator(handler: Callable):
        def wrapped_handler(sid: str, *args):
            try:
                return handler(sid, *args)
            except Exception as e:
                logger.error(e)
                sio.send(str(e), to=sid)

        sio.on(event, wrapped_handler)
        return wrapped_handler

    return sio_on_decorator


debug_path = "/zundamahjong"
debug_app = WSGIApp(
    sio,
    static_files={
        f"{debug_path}/": {
            "filename": "./static/index.html",
            "content_type": "text/html",
        },
        f"{debug_path}/mahjongtiles": {
            "filename": "./static/mahjongtiles",
            "content_type": "image/svg+xml",
        },
        f"{debug_path}/js": {
            "filename": "./static/js",
            "content_type": "text/javascript",
        },
        f"{debug_path}/style": {
            "filename": "./static/style",
            "content_type": "text/css",
        },
    },
)

app = WSGIApp(sio)
