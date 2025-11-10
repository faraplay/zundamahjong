from collections import deque
from collections.abc import Sequence

from pydantic import BaseModel

from .tile import TileId


class Discard(BaseModel):
    player: int
    tile: TileId
    is_riichi: bool


class DiscardPool:
    def __init__(self) -> None:
        self._discards: deque[Discard] = deque()

    @property
    def discards(self) -> Sequence[Discard]:
        return self._discards

    def append(self, player: int, tile: TileId, is_riichi: bool) -> None:
        self._discards.append(Discard(player=player, tile=tile, is_riichi=is_riichi))

    def pop(self) -> Discard:
        return self._discards.pop()
