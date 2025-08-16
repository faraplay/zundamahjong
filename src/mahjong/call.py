from enum import Enum

from .tile import Tile


class CallType(Enum):
    CHI = 1
    PON = 2
    OPEN_KAN = 3
    ADD_KAN = 4
    CLOSED_KAN = 5
    FLOWER = 6


class Call:
    def __init__(self, call_type: CallType, tiles: list[Tile]):
        self._call_type = call_type
        self._tiles = tiles

    @property
    def call_type(self):
        return self._call_type

    @property
    def tiles(self):
        return tuple(self._tiles)

    def add_kan(self):
        assert self._call_type == CallType.PON
        self._call_type = CallType.ADD_KAN
        self._tiles.append(self._tiles[0])
