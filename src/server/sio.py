from collections.abc import Callable

from socketio import Server, WSGIApp

sio = Server(logger=True, async_mode="threading")


def sio_on(event: str):
    def sio_on_decorator(handler: Callable):
        def wrapped_handler(sid: str, *args):
            try:
                return handler(sid, *args)
            except Exception as e:
                print(e)
                sio.send(str(e), to=sid)

        sio.on(event, wrapped_handler)
        return wrapped_handler

    return sio_on_decorator


debug_app = WSGIApp(
    sio,
    static_files={
        "/static/index.html": {
            "filename": "./static/index.html",
            "content_type": "text/html",
        },
        "/static/mahjongtiles": {
            "filename": "./static/mahjongtiles",
            "content_type": "image/svg+xml",
        },
        "/static/js": {"filename": "./static/js", "content_type": "text/javascript"},
        "/static/style": {"filename": "./static/style", "content_type": "text/css"},
    },
)

app = WSGIApp(sio)
