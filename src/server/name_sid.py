from threading import Lock

from flask_socketio import emit

name_to_sid: dict[str, str] = {}
sid_to_name: dict[str, str] = {}
name_sid_lock = Lock()


def set_name(sid: str, name: str):
    with name_sid_lock:
        if name_to_sid.get(name, sid) != sid:
            emit("name_in_use_error")
        else:
            old_name = sid_to_name.get(sid, None)
            if old_name:
                name_to_sid.pop(old_name)
            name_to_sid[name] = sid
            sid_to_name[sid] = name
            emit("set_name_success")


def remove_sid(sid: str):
    with name_sid_lock:
        name = sid_to_name.get(sid, None)
        if name:
            name_to_sid.pop(name)
            sid_to_name.pop(sid)


def emit_to_name(event, *args, name: str):
    sid = name_to_sid.get(name, None)
    if sid:
        emit(event, *args, to=sid)
