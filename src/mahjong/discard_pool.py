from pydantic import BaseModel

from collections import deque
from collections.abc import Sequence

from .tile import Tile


class Discard(BaseModel):
    seat: int
    tile: Tile


class DiscardPool:
    def __init__(self):
        self._discards: deque[Discard] = deque()

    @property
    def discards(self) -> Sequence[Discard]:
        return self._discards

    def append(self, seat: int, tile: Tile):
        self._discards.append(Discard(seat=seat, tile=tile))

    def pop(self):
        return self._discards.pop()

    def peek(self):
        try:
            return self._discards[-1]
        except IndexError:
            return 0
