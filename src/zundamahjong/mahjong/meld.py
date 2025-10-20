from enum import IntEnum
from typing import Optional
from pydantic import BaseModel

from .tile import TileId, TileValue


class MeldType(IntEnum):
    CHI = 0
    PON = 1
    KAN = 2
    PAIR = 3
    THIRTEEN_ORPHANS = 4


class TileValueMeld(BaseModel):
    meld_type: MeldType
    tiles: list[TileValue]
    winning_tile_index: Optional[int] = None


class Meld(BaseModel):
    meld_type: MeldType
    tiles: list[TileId]
    winning_tile_index: Optional[int] = None
