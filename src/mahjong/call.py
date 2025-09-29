from enum import IntEnum
from pydantic import BaseModel

from .tile import TileId


class CallType(IntEnum):
    PAIR = 0
    CHI = 1
    PON = 2
    OPEN_KAN = 3
    ADD_KAN = 4
    CLOSED_KAN = 5
    THIRTEEN_ORPHANS = 6


class Call(BaseModel):
    call_type: CallType
    tiles: list[TileId]
