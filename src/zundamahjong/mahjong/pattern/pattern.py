from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from typing import final

from pydantic import BaseModel

from ..call import CallType, get_call_tiles, get_meld_type
from ..meld import Meld, MeldType, TileValueMeld
from ..tile import (
    get_tile_value,
    is_number,
    orphans,
)
from ..win import Win
from .wait_pattern import get_wait_pattern


class PatternData(BaseModel):
    """
    Represents a pattern and its han and fu values.
    """

    display_name: str
    "The name of the pattern."
    han: int
    "The han value of the pattern."
    fu: int
    "The fu value of the pattern."


default_pattern_data: dict[str, PatternData] = {}
"""
A dictionary containing :py:class:`PatternData` objects
with all the default han and fu values.

Patterns are indexed by the internal names of the patterns
(in SCREAMING_SNAKE_CASE).
"""
pattern_mult_funcs: dict[str, Callable[[PatternCalculator], int]] = {}
"""
A dictionary containing a :py:class:`PatternCalculator` method for each pattern.

Each method calculates the number of times a pattern applies to the
hand stored in the :py:class:`PatternCalculator` object.
Usually the number of times a pattern applies is 0 or 1, but for some
patterns (e.g. ``SEAT_FLOWER``) the pattern can apply with multiplicity
(i.e. more than once).

Patterns are indexed by the internal names of the patterns
(in SCREAMING_SNAKE_CASE).
"""


def register_pattern(
    name: str, display_name: str, han: int, fu: int
) -> Callable[[Callable[[PatternCalculator], int]], Callable[[PatternCalculator], int]]:
    default_pattern_data[name] = PatternData(display_name=display_name, han=han, fu=fu)
    """
    Decorator to register a :py:class:`PatternCalculator` method as a method
    that calculates a pattern's multiplicity.

    :param name: The internal name of the pattern. This should be in
                 SCREAMING_SNAKE_CASE.
    :param display_name: The name of the pattern to display.
    :param han: The default han value of the pattern.
    :param fu: The default fu value of the pattern.
    """

    def _register_pattern_inner(
        func: Callable[[PatternCalculator], int],
    ) -> Callable[[PatternCalculator], int]:
        pattern_mult_funcs[name] = func
        return func

    return _register_pattern_inner


@final
class PatternCalculator:
    """
    Class to calculate the patterns in a winning hand.
    Use the method :py:meth:`get_pattern_mults` to get the patterns.

    :param win: The :py:class:`Win` object with the winning hand.
    :param formed_hand: A list containing the winning hand's tiles arranged into
                        :py:class:`Meld` s.
    """

    def __init__(self, win: Win, formed_hand: list[Meld]) -> None:
        self.win = win
        self.formed_hand = formed_hand

        self._count_melds()

        self.is_closed_hand = all(
            call.call_type == CallType.CLOSED_KAN for call in self.win.calls
        )
        self.seat = (self.win.win_player - self.win.sub_round) % self.win.player_count
        self.flowers = set(get_tile_value(flower) for flower in self.win.flowers)
        self.melds = [
            TileValueMeld(
                meld_type=meld.meld_type,
                tiles=[get_tile_value(tile) for tile in meld.tiles],
                winning_tile_index=meld.winning_tile_index,
            )
            for meld in self.formed_hand
        ] + [
            TileValueMeld(
                meld_type=get_meld_type(call.call_type),
                tiles=[get_tile_value(tile) for tile in get_call_tiles(call)],
                winning_tile_index=None,
            )
            for call in self.win.calls
        ]
        winning_meld = next(
            meld for meld in self.melds if meld.winning_tile_index is not None
        )
        assert winning_meld.winning_tile_index is not None
        self.winning_tile = winning_meld.tiles[winning_meld.winning_tile_index]
        self.wait_pattern = get_wait_pattern(winning_meld)
        self.hand_tiles = [tile for call in self.melds for tile in call.tiles]
        self.used_suits = set((tile // 10) * 10 for tile in self.hand_tiles)
        self.call_outsidenesses = set(
            self._is_outside_call(meld) for meld in self.melds
        )
        self.chii_start_tiles = Counter(
            call.tiles[0] for call in self.melds if call.meld_type == MeldType.CHI
        )
        self.concealed_triplets = sum(
            tile_meld.meld_type == MeldType.PON
            and (tile_meld.winning_tile_index is None or self.win.lose_player is None)
            for tile_meld in self.formed_hand
        ) + sum(call.call_type == CallType.CLOSED_KAN for call in self.win.calls)
        self.quads = sum(call.meld_type == MeldType.KAN for call in self.melds)
        self.triplet_tiles = {
            call.tiles[0]
            for call in self.melds
            if call.meld_type in self._triplet_types
        }

    _triplet_types = {MeldType.PON, MeldType.KAN}
    _number_suits = [0, 10, 20]
    _honour_suit = 30

    def _count_melds(self) -> None:
        self.pair_count = 0
        self.pair_tile = 0
        self.chii_meld_count = 0
        self.simple_open_triplet_count = 0
        self.orphan_open_triplet_count = 0
        self.simple_closed_triplet_count = 0
        self.orphan_closed_triplet_count = 0
        self.simple_open_quad_count = 0
        self.orphan_open_quad_count = 0
        self.simple_closed_quad_count = 0
        self.orphan_closed_quad_count = 0
        for meld in self.formed_hand:
            if meld.meld_type == MeldType.CHI:
                self.chii_meld_count += 1
            elif meld.meld_type == MeldType.PON:
                if (
                    meld.winning_tile_index is not None
                    and self.win.lose_player is not None
                ):
                    if get_tile_value(meld.tiles[0]) not in orphans:
                        self.simple_open_triplet_count += 1
                    else:
                        self.orphan_open_triplet_count += 1
                else:
                    if get_tile_value(meld.tiles[0]) not in orphans:
                        self.simple_closed_triplet_count += 1
                    else:
                        self.orphan_closed_triplet_count += 1
            elif meld.meld_type == MeldType.KAN:
                raise Exception("Unexpected kan meld in formed hand!")
            elif meld.meld_type == MeldType.PAIR:
                self.pair_count += 1
                self.pair_tile = get_tile_value(meld.tiles[0])

        for call in self.win.calls:
            if call.call_type == CallType.CHI:
                self.chii_meld_count += 1
            elif call.call_type == CallType.PON:
                if get_tile_value(call.called_tile) not in orphans:
                    self.simple_open_triplet_count += 1
                else:
                    self.orphan_open_triplet_count += 1
            elif (
                call.call_type == CallType.OPEN_KAN
                or call.call_type == CallType.ADD_KAN
            ):
                if get_tile_value(call.called_tile) not in orphans:
                    self.simple_open_quad_count += 1
                else:
                    self.orphan_open_quad_count += 1
            elif call.call_type == CallType.CLOSED_KAN:
                if get_tile_value(call.tiles[0]) not in orphans:
                    self.simple_closed_quad_count += 1
                else:
                    self.orphan_closed_quad_count += 1

    def _is_outside_call(self, meld: TileValueMeld) -> int:
        "Returns 2 if it contains a terminal, 1 if it contains an honor, 0 otherwise"
        tile = meld.tiles[0]
        if meld.meld_type == MeldType.CHI:
            if tile % 10 == 1 or tile % 10 == 7:
                return 2
            else:
                return 0
        elif meld.meld_type == MeldType.THIRTEEN_ORPHANS:
            return 0
        else:
            if not is_number(tile):
                return 1
            elif tile % 10 == 1 or tile % 10 == 9:
                return 2
            else:
                return 0
