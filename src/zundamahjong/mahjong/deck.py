from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from random import shuffle
from typing import final

from .tile import N, TileId

four_player_deck: list[TileId] = [
    tile_value * N + r
    for tile_value in (
        list(range(1, 10))
        + list(range(11, 20))
        + list(range(21, 30))
        + list(range(31, 38))
    )
    for r in range(4)
] + [tile_value * N for tile_value in (list(range(41, 49)))]

three_player_deck: list[TileId] = [
    tile_value * N + r
    for tile_value in (
        [1, 9] + list(range(11, 20)) + list(range(21, 30)) + list(range(31, 38))
    )
    for r in range(4)
] + [tile_value * N for tile_value in [41, 42, 43, 45, 46, 47]]


@final
class Deck:
    def __init__(self, tiles: Iterable[TileId]) -> None:
        self._tiles = deque(tiles)

    @classmethod
    def shuffled_deck(cls, tiles: list[TileId]) -> Deck:
        new_deck = tiles.copy()
        shuffle(new_deck)
        return cls(new_deck)

    @property
    def tiles(self) -> tuple[TileId, ...]:
        return tuple(self._tiles)

    def pop(self) -> TileId:
        return self._tiles.popleft()

    def popleft(self) -> TileId:
        return self._tiles.pop()
