from enum import IntEnum
from pydantic import BaseModel

from src.mahjong.tile import TileId, TileValue


class MeldType(IntEnum):
    PAIR = 0
    CHI = 1
    PON = 2
    OPEN_KAN = 3
    ADD_KAN = 4
    CLOSED_KAN = 5
    THIRTEEN_ORPHANS = 6


class TileValueMeld(BaseModel):
    meld_type: MeldType
    tiles: list[TileValue]


class Meld(BaseModel):
    meld_type: MeldType
    tiles: list[TileId]
