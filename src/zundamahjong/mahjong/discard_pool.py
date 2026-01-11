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
    called: bool
    "Whether the discarded tile has been called."
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

    @property
    def last_discarded_tile(self) -> TileId | None:
        """
        The :py:class:`TileId` of the last discarded tile, or ``None`` if the
        last discarded tile has been called.
        """
        if len(self._discards) == 0:
            return None
        last_discard = self._discards[-1]
        if last_discard.called:
            return None
        return last_discard.tile

    def append(self, player: int, tile: TileId, is_riichi: bool) -> None:
        """
        Add a tile to the discard pool.

        :param player: The index of the player who discarded the tile.
        :param tile: The :py:class:`TileId` of the discarded tile.
        :param is_riichi: Whether the player was in riichi when they discarded the tile.
        """
        self._discards.append(
            Discard(player=player, tile=tile, is_riichi=is_riichi, called=False)
        )

    def pop(self) -> TileId:
        """
        Set the last discarded tile to the called state.

        :return: The :py:class:`TileId` representing the last discarded tile.
        """
        last_discard = self._discards[-1]
        last_discard.called = True
        return last_discard.tile
