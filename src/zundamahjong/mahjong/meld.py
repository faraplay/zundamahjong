from enum import IntEnum

from pydantic import BaseModel

from .tile import TileId, TileValue


class MeldType(IntEnum):
    "Enum representing the type of meld (chii, pon, kan, pair, a thirteen orphans hand)"

    CHI = 0
    PON = 1
    KAN = 2
    PAIR = 3
    THIRTEEN_ORPHANS = 4


class TileValueMeld(BaseModel):
    "Represents the TileValues of a meld."

    meld_type: MeldType
    "The :py:class:`MeldType` of the meld."
    tiles: list[TileValue]
    "A list of the :py:class:`TileValue` s of the tiles in the meld."
    winning_tile_index: int | None = None
    """
    If the winning tile is in this meld, this is the index of the
    winning tile in ``tiles``. Otherwise it is `None`.
    """


class Meld(BaseModel):
    "Represents a meld."

    meld_type: MeldType
    "The :py:class:`MeldType` of the meld."
    tiles: list[TileId]
    "A list of the :py:class:`TileId` s in the meld."
    winning_tile_index: int | None = None
    """
    If the winning tile is in this meld, this is the index of the
    winning tile in ``tiles``. Otherwise it is `None`.
    """
