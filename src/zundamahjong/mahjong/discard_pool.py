from collections import deque
from collections.abc import Sequence

from pydantic import BaseModel

from .tile import TileId


class Discard(BaseModel):
    """
    Represents a discarded tile.

    Also represents a tile added to a kan or used to form a closed kan,
    since those tiles can be won off of.
    """

    player: int
    "The index of the player who discarded the tile."
    tile: TileId
    "The :py:class:`TileId` of the discarded tile."
    is_called: bool
    "Whether the discarded tile has been called."
    is_kan: bool
    "Whether the tile was part of an added kan or closed kan."


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
        if last_discard.is_called:
            return None
        return last_discard.tile

    def append(self, player: int, tile: TileId, *, is_kan: bool = False) -> None:
        """
        Add a tile to the discard pool.

        :param player: The index of the player who discarded the tile.
        :param tile: The :py:class:`TileId` of the discarded tile.
        :param is_riichi: Whether the player was in riichi when they discarded the tile.
        :param is_kan: (Defaults to false) Whether the tile was actually part of a kan
                       instead of being discarded.
        """
        self._discards.append(
            Discard(player=player, tile=tile, is_called=False, is_kan=is_kan)
        )

    def pop(self) -> TileId:
        """
        Set the last discarded tile to the called state.

        :return: The :py:class:`TileId` representing the last discarded tile.
        """
        last_discard = self._discards[-1]
        last_discard.is_called = True
        return last_discard.tile
