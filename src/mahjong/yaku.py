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

        self._flowers = {
            call.tiles[0] for call in win.calls if call.call_type == CallType.FLOWER
        }

    def get_yaku_mults(self):
        yaku_mults: dict[str, int] = {}
        for yaku, get_yaku_multiplicity in yaku_mult_funcs.items():
            yaku_mult = get_yaku_multiplicity(self)
            if yaku_mult != 0:
                yaku_mults[yaku] = yaku_mult
        return yaku_mults

    @_register_yaku("THIRTEEN_ORPHANS", "Thirteen Orphans", 13)
    def _thirteen_orphans(self):
        return int(
            len(self._formed_hand) == 1
            and self._formed_hand[0].call_type == CallType.THIRTEEN_ORPHANS
        )

    @_register_yaku("SEVEN_PAIRS", "Seven Pairs", 3)
    def _seven_pairs(self):
        return len(self._formed_hand) == 7 and int(
            all(call.call_type == CallType.PAIR for call in self._formed_hand)
        )

    def _yakuhai(self, yaku_tile):
        return int(
            any(
                (call.tiles[0] == yaku_tile and call.call_type != CallType.PAIR)
                for call in self._formed_hand + self._win.calls
            )
        )

    @_register_yaku("SEAT_WIND", "Seat Wind", 1)
    def _seat_wind(self):
        return self._yakuhai(self._win.win_seat + 31)

    @_register_yaku("PREVALENT_WIND", "Prevalent Wind", 1)
    def _prevalent_wind(self):
        return self._yakuhai(self._win.wind_round + 31)

    @_register_yaku("WHITE_DRAGON", "White Dragon", 1)
    def _white_dragon(self):
        return self._yakuhai(35)

    @_register_yaku("GREEN_DRAGON", "Green Dragon", 1)
    def _green_dragon(self):
        return self._yakuhai(36)

    @_register_yaku("RED_DRAGON", "Red Dragon", 1)
    def _red_dragon(self):
        return self._yakuhai(37)

    @_register_yaku("EYES", "Eyes", 1)
    def _eyes(self):
        pairs = [call for call in self._formed_hand if call.call_type == CallType.PAIR]
        if len(pairs) != 1:
            return 0
        tile = pairs[0].tiles[0]
        if not is_number(tile):
            return 0
        return int((tile % 10) % 3 == 2)

    @_register_yaku("NO_CALLS", "No Calls", 1)
    def _no_calls(self):
        return int(
            not self._seven_pairs()
            and not self._thirteen_orphans()
            and all(
                call.call_type == CallType.FLOWER
                or call.call_type == CallType.CLOSED_KAN
                for call in self._win.calls
            )
        )

    @_register_yaku("NO_FLOWERS", "No Flowers", 1)
    def _no_flowers(self):
        return int(len(self._flowers) == 0)

    @_register_yaku("SEAT_FLOWER", "Seat Flower", 1)
    def _seat_flower(self):
        return sum((tile - 41) % 4 == self._win.win_seat for tile in self._flowers)

    @_register_yaku("SET_OF_FLOWERS", "Set of Flowers", 2)
    def _set_of_flowers(self):
        return int(
            ({41, 42, 43, 44} <= self._flowers) or ({45, 46, 47, 48} <= self._flowers)
        )

    @_register_yaku("SEVEN_FLOWERS", "Seven Flowers", 2)
    def _seven_flowers(self):
        return int(len(self._flowers) == 7)

    @_register_yaku("TWO_SETS_OF_FLOWERS", "Two Sets of Flowers", 8)
    def _two_sets_of_flowers(self):
        return int(len(self._flowers) == 8)

    @_register_yaku("AFTER_A_FLOWER", "After a Flower", 1)
    def _after_a_flower(self):
        return self._win.after_flower_count

    @_register_yaku("AFTER_A_KAN", "After a Kan", 2)
    def _after_a_kan(self):
        return self._win.after_kan_count
