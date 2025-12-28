from collections import deque
from collections.abc import Sequence

from pydantic import BaseModel

from .tile import TileId


class Discard(BaseModel):
    "Represents a discarded tile."

    player: int
    "The index of the player who discarded the tile."
    tile: TileId
    "The :py:class:`TileId` of the discarded tile."
    is_riichi: bool
    "Whether the player was in riichi when they discarded the tile."


class DiscardPool:
    "Represents the list of discarded tiles in a round of mahjong."

    def __init__(self) -> None:
        self._discards: deque[Discard] = deque()

    @property
    def discards(self) -> Sequence[Discard]:
        "A sequence of :py:class:`Discard` s representing the discarded tiles."
        return self._discards

    def append(self, player: int, tile: TileId, is_riichi: bool) -> None:
        """
        Add a tile to the discard pool.

        :param player: The index of the player who discarded the tile.
        :param tile: The :py:class:`TileId` of the discarded tile.
        :param is_riichi: Whether the player was in riichi when they discarded the tile.
        """
        self._discards.append(Discard(player=player, tile=tile, is_riichi=is_riichi))

    def pop(self) -> Discard:
        """
        Remove the last discarded tile from the discard pool.

        :return: The :py:class:`Discard` representing the last discard.
        """
        return self._discards.pop()
