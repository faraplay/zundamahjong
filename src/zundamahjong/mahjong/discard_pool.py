from collections import deque
from collections.abc import Sequence

from pydantic import BaseModel

from .tile import TileId


class Discard(BaseModel):
    player: int
    tile: TileId


class DiscardPool:
    def __init__(self) -> None:
        self._discards: deque[Discard] = deque()

    @property
    def discards(self) -> Sequence[Discard]:
        return self._discards

    def append(self, player: int, tile: TileId) -> None:
        self._discards.append(Discard(player=player, tile=tile))

    def pop(self) -> Discard:
        return self._discards.pop()
