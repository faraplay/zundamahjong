from collections.abc import Iterable
from random import shuffle
from collections import deque

from .tile import Tile, N

four_player_deck: list[Tile] = [
    tile_value * N + r
    for tile_value in (
        list(range(1, 10))
        + list(range(11, 20))
        + list(range(21, 30))
        + list(range(31, 38))
    )
    for r in range(4)
] + [tile_value * N for tile_value in (list(range(41, 49)))]

three_player_deck: list[Tile] = [
    tile_value * N + r
    for tile_value in (
        [1, 9] + list(range(11, 20)) + list(range(21, 30)) + list(range(31, 38))
    )
    for r in range(4)
] + [tile_value * N for tile_value in [41, 42, 43, 45, 46, 47]]


class Deck:
    def __init__(self, tiles: Iterable[Tile]):
        self._tiles = deque(tiles)

    @classmethod
    def shuffled_deck(cls, tiles: list[Tile]):
        new_deck = tiles.copy()
        shuffle(new_deck)
        return cls(new_deck)

    @property
    def tiles(self):
        return tuple(self._tiles)

    def pop(self):
        return self._tiles.popleft()

    def popleft(self):
        return self._tiles.pop()
