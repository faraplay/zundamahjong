from enum import Enum
from typing import NamedTuple

from .tile import Tile


class CallType(Enum):
    PAIR = 0
    CHI = 1
    PON = 2
    OPEN_KAN = 3
    ADD_KAN = 4
    CLOSED_KAN = 5
    FLOWER = 6


class Call(NamedTuple):
    call_type: CallType
    tiles: list[Tile]
