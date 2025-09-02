from enum import StrEnum
from pydantic import BaseModel

from .tile import Tile, is_number
from .call import Call, CallType


class Win(BaseModel):
    win_seat: int
    lose_seat: int | None
    hand: list[Tile]
    calls: list[Call]


class Yaku(StrEnum):
    EYES = "eyes"
    SEVEN_PAIRS = "seven pairs"
    THIRTEEN_ORPHANS = "thirteen orphans"


class YakuHan(BaseModel):
    yaku: Yaku
    han: int


default_yaku_values = {Yaku.EYES: 1, Yaku.SEVEN_PAIRS: 3, Yaku.THIRTEEN_ORPHANS: 13}


class YakuCalculator:
    def __init__(self, win: Win, formed_hand: list[Call]):
        self._win = win
        self._formed_hand = formed_hand

    def get_yakus(self):
        yakus: list[Yaku] = []
        for yaku, is_yaku in self.is_yaku_functions.items():
            if is_yaku(self):
                yakus.append(yaku)
        return yakus

    def _is_seven_pairs(self):
        return len(self._formed_hand) == 7 and all(
            call.call_type == CallType.PAIR for call in self._formed_hand
        )

    def _is_thirteen_orphans(self):
        return (
            len(self._formed_hand) == 1
            and self._formed_hand[0].call_type == CallType.THIRTEEN_ORPHANS
        )

    def _is_eyes(self):
        pairs = [call for call in self._formed_hand if call.call_type == CallType.PAIR]
        if len(pairs) != 1:
            return False
        tile = pairs[0].tiles[0]
        if not is_number(tile):
            return False
        return (tile % 10) % 3 == 2

    is_yaku_functions = {
        Yaku.EYES: _is_eyes,
        Yaku.SEVEN_PAIRS: _is_seven_pairs,
        Yaku.THIRTEEN_ORPHANS: _is_thirteen_orphans,
    }
