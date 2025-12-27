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
]
"""
A list of :py:class:`TileId` s of the tiles used in a four-player deck
without flowers.
"""
four_player_flowers: list[TileId] = [
    tile_value * N for tile_value in (list(range(41, 49)))
]
"""
A list of :py:class:`TileId` s of the flowers used in a four-player deck.
"""

three_player_deck: list[TileId] = [
    tile_value * N + r
    for tile_value in (
        [1, 9] + list(range(11, 20)) + list(range(21, 30)) + list(range(31, 38))
    )
    for r in range(4)
]
"""
A list of :py:class:`TileId` s of the tiles used in a three-player deck
without flowers.
"""
three_player_flowers: list[TileId] = [
    tile_value * N for tile_value in [41, 42, 43, 45, 46, 47]
]
"""
A list of :py:class:`TileId` s of the flowers used in a three-player deck.
"""


@final
class Deck:
    """
    A class representing the deck in a round of mahjong.

    :param tiles: List of :py:class:`TileId` s that the :py:class:`Deck`
                  will contain.
    """

    def __init__(self, tiles: Iterable[TileId]) -> None:
        self._tiles = deque(tiles)

    @classmethod
    def shuffled_deck(cls, tiles: list[TileId]) -> Deck:
        """
        Creates a new :py:class:`Deck` containing the given list of
        :py:class:`TileId` s, shuffled.

        :param tiles: A list of the :py:class:`TileId` s the new
                      :py:class:`Deck` will contain.
        """
        new_deck = tiles.copy()
        shuffle(new_deck)
        return cls(new_deck)

    @property
    def tiles(self) -> tuple[TileId, ...]:
        "Returns the list of :py:class:`TileId` s remaining in the deck."
        return tuple(self._tiles)

    def pop(self) -> TileId:
        """
        Removes the first remaining tile of the deck, and returns its
        :py:class:`TileId`."""
        return self._tiles.popleft()

    def popleft(self) -> TileId:
        """
        Removes the tile at the back of the deck, and returns its
        :py:class:`TileId`.
        """
        return self._tiles.pop()
