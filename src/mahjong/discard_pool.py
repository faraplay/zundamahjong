from collections import deque

from .tile import Tile


class DiscardPool:
    def __init__(self):
        self._tiles: deque[Tile] = deque()

    @property
    def tiles(self):
        return tuple(self._tiles)

    def append(self, tile: Tile):
        self._tiles.append(tile)

    def pop(self):
        return self._tiles.pop()

    def peek(self):
        try:
            return self._tiles[-1]
        except IndexError:
            return 0
