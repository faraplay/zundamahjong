from collections.abc import Iterable
from random import shuffle
from collections import deque

from .tile import Tile

four_player_deck: list[Tile] = (
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    + [11, 12, 13, 14, 15, 16, 17, 18, 19]
    + [21, 22, 23, 24, 25, 26, 27, 28, 29]
    + [31, 32, 33, 34, 35, 36, 37]
) * 4 + [41, 42, 43, 44, 45, 46, 47, 48]

three_player_deck: list[Tile] = (
    [1, 9]
    + [11, 12, 13, 14, 15, 16, 17, 18, 19]
    + [21, 22, 23, 24, 25, 26, 27, 28, 29]
    + [31, 32, 33, 34, 35, 36, 37]
) * 4 + [41, 42, 43, 45, 46, 47]


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
