from collections.abc import Iterable
from random import shuffle
from collections import deque

from .tile import Tile

four_player_deck: list[Tile] = (
    list(range(4, 40))
    + list(range(44, 80))
    + list(range(84, 120))
    + list(range(124, 152))
    + list(range(164, 196, 4))
)

three_player_deck: list[Tile] = (
    list(range(4, 8))
    + list(range(36, 40))
    + list(range(44, 80))
    + list(range(84, 120))
    + list(range(124, 152))
    + list(range(164, 176, 4))
    + list(range(180, 192, 4))
)


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
