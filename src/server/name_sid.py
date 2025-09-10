from threading import Lock

from flask_socketio import emit

name_to_sid: dict[str, str] = {}
sid_to_name: dict[str, str] = {}
name_sid_lock = Lock()


def verify_name(name: str):
    if not isinstance(name, str):
        raise Exception("Name is not a string!")
    if len(name) > 20:
        raise Exception("Name is over 20 characters long!")
    if name == "":
        raise Exception("Name cannot be empty!")


def get_name(sid: str):
    try:
        return sid_to_name[sid]
    except KeyError:
        raise Exception("Client has no name set!")


def set_name(sid: str, name: str):
    with name_sid_lock:
        if name_to_sid.get(name, sid) != sid:
            raise Exception("Name is already in use!")
        old_name = sid_to_name.get(sid, None)
        if old_name:
            name_to_sid.pop(old_name)
        name_to_sid[name] = sid
        sid_to_name[sid] = name


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
