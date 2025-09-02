from pydantic import BaseModel

from .tile import Tile, is_number
from .call import Call, CallType


class Win(BaseModel):
    win_seat: int
    lose_seat: int | None
    hand: list[Tile]
    calls: list[Call]


class YakuHan(BaseModel):
    yaku: str
    han: int


yaku_display_names: dict[str, str] = {}
default_yaku_han: dict[str, int] = {}
is_yaku_functions = {}


def _register_yaku(name: str, display_name: str, han: int):
    yaku_display_names[name] = display_name
    default_yaku_han[name] = han

    def _register_yaku_inner(func):
        is_yaku_functions[name] = func
        return func

    return _register_yaku_inner


class YakuCalculator:
    def __init__(self, win: Win, formed_hand: list[Call]):
        self._win = win
        self._formed_hand = formed_hand

    def get_yakus(self):
        yakus = []
        for yaku, is_yaku in is_yaku_functions.items():
            if is_yaku(self):
                yakus.append(yaku)
        return yakus

    @_register_yaku("SEVEN_PAIRS", "Seven Pairs", 3)
    def _is_seven_pairs(self):
        return len(self._formed_hand) == 7 and all(
            call.call_type == CallType.PAIR for call in self._formed_hand
        )

    @_register_yaku("THIRTEEN_ORPHANS", "Thirteen Orphans", 13)
    def _is_thirteen_orphans(self):
        return (
            len(self._formed_hand) == 1
            and self._formed_hand[0].call_type == CallType.THIRTEEN_ORPHANS
        )

    @_register_yaku("EYES", "Eyes", 1)
    def _is_eyes(self):
        pairs = [call for call in self._formed_hand if call.call_type == CallType.PAIR]
        if len(pairs) != 1:
            return False
        tile = pairs[0].tiles[0]
        if not is_number(tile):
            return False
        return (tile % 10) % 3 == 2
