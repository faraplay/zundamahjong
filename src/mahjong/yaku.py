from __future__ import annotations
from collections.abc import Callable

from .tile import is_number
from .call import Call, CallType
from .win import Win

yaku_display_names: dict[str, str] = {}
default_yaku_han: dict[str, int] = {}
yaku_mult_funcs: dict[str, Callable[[YakuCalculator], int]] = {}


def _register_yaku(name: str, display_name: str, han: int):
    yaku_display_names[name] = display_name
    default_yaku_han[name] = han

    def _register_yaku_inner(func: Callable[[YakuCalculator], int]):
        yaku_mult_funcs[name] = func
        return func

    return _register_yaku_inner


class YakuCalculator:
    def __init__(self, win: Win, formed_hand: list[Call]):
        self._win = win
        self._formed_hand = formed_hand

    def get_yaku_mults(self):
        yaku_mults: dict[str, int] = {}
        for yaku, get_yaku_multiplicity in yaku_mult_funcs.items():
            yaku_mult = get_yaku_multiplicity(self)
            if yaku_mult != 0:
                yaku_mults[yaku] = yaku_mult
        return yaku_mults

    @_register_yaku("SEVEN_PAIRS", "Seven Pairs", 3)
    def _seven_pairs(self):
        return len(self._formed_hand) == 7 and int(
            all(call.call_type == CallType.PAIR for call in self._formed_hand)
        )

    @_register_yaku("THIRTEEN_ORPHANS", "Thirteen Orphans", 13)
    def _thirteen_orphans(self):
        return int(
            len(self._formed_hand) == 1
            and self._formed_hand[0].call_type == CallType.THIRTEEN_ORPHANS
        )

    @_register_yaku("EYES", "Eyes", 1)
    def _eyes(self):
        pairs = [call for call in self._formed_hand if call.call_type == CallType.PAIR]
        if len(pairs) != 1:
            return 0
        tile = pairs[0].tiles[0]
        if not is_number(tile):
            return 0
        return int((tile % 10) % 3 == 2)
