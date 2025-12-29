from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from typing import final

from pydantic import BaseModel

from ..call import CallType, get_call_tiles, get_meld_type
from ..meld import Meld, MeldType, TileValueMeld
from ..tile import (
    TileValue,
    dragons,
    get_tile_value,
    green_tiles,
    is_number,
    orphans,
    terminals,
    winds,
)
from ..win import Win

from .wait_pattern import WaitPattern, get_wait_pattern


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

    @register_pattern(
        "BLESSING_OF_HEAVEN",
        display_name="Blessing of Heaven",
        han=20,
        fu=0,
    )
    def blessing_of_heaven(self: PatternCalculator) -> int:
        return int(self.win.is_tenhou)

    @register_pattern(
        "BLESSING_OF_EARTH",
        display_name="Blessing of Earth",
        han=19,
        fu=0,
    )
    def blessing_of_earth(self: PatternCalculator) -> int:
        return int(self.win.is_chiihou)

    @register_pattern(
        "LITTLE_THREE_DRAGONS",
        display_name="Little Three Dragons",
        han=5,
        fu=0,
    )
    def little_three_dragons(self: PatternCalculator) -> int:
        total = 0
        for tile in dragons:
            tile_count = self.hand_tiles.count(tile)
            if tile_count == 4:
                tile_count = 3
            total += tile_count
        return int(total == 8)

    @register_pattern(
        "BIG_THREE_DRAGONS",
        display_name="Big Three Dragons",
        han=8,
        fu=0,
    )
    def big_three_dragons(self: PatternCalculator) -> int:
        return dragons <= self.triplet_tiles

    @register_pattern(
        "FOUR_LITTLE_WINDS",
        display_name="Four Little Winds",
        han=12,
        fu=0,
    )
    def four_little_winds(self: PatternCalculator) -> int:
        total = 0
        for tile in winds:
            tile_count = self.hand_tiles.count(tile)
            if tile_count == 4:
                tile_count = 3
            total += tile_count
        return int(total == 11)

    @register_pattern(
        "FOUR_BIG_WINDS",
        display_name="Four Big Winds",
        han=16,
        fu=0,
    )
    def four_big_winds(self: PatternCalculator) -> int:
        return int(winds <= self.triplet_tiles)

    @register_pattern(
        "FOUR_CONCEALED_TRIPLETS",
        display_name="Four Concealed Triplets",
        han=12,
        fu=0,
    )
    def four_concealed_triplets(self: PatternCalculator) -> int:
        return int(
            self.concealed_triplets == 4 and self.wait_pattern == WaitPattern.SHANPON
        )

    @register_pattern(
        "FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT",
        display_name="Four Concealed Triplets 1-sided Wait",
        han=12,
        fu=0,
    )
    def four_concealed_triplets_1_sided_wait(self: PatternCalculator) -> int:
        return int(
            self.concealed_triplets == 4 and self.wait_pattern == WaitPattern.TANKI
        )

    @register_pattern(
        "ALL_HONOURS",
        display_name="All Honours",
        han=10,
        fu=0,
    )
    def all_honours(self: PatternCalculator) -> int:
        return int(self.used_suits == {self._honour_suit})

    @register_pattern(
        "ALL_GREENS",
        display_name="All Greens",
        han=16,
        fu=0,
    )
    def all_greens(self: PatternCalculator) -> int:
        return int(all(tile in green_tiles for tile in self.hand_tiles))

    @register_pattern(
        "ALL_TERMINALS",
        display_name="All Terminals",
        han=13,
        fu=0,
    )
    def all_terminals(self: PatternCalculator) -> int:
        return int(all(tile in terminals for tile in self.hand_tiles))

    @register_pattern(
        "THIRTEEN_ORPHANS",
        display_name="Thirteen Orphans",
        han=13,
        fu=0,
    )
    def thirteen_orphans(self: PatternCalculator) -> int:
        return int(self.wait_pattern == WaitPattern.KOKUSHI)

    @register_pattern(
        "THIRTEEN_ORPHANS_13_SIDED_WAIT",
        display_name="Thirteen Orphans 13-sided Wait",
        han=13,
        fu=0,
    )
    def thirteen_orphans_13_sided_wait(self: PatternCalculator) -> int:
        return int(self.wait_pattern == WaitPattern.KOKUSHI_13)

    @register_pattern(
        "FOUR_QUADS",
        display_name="Four Quads",
        han=18,
        fu=0,
    )
    def four_quads(self: PatternCalculator) -> int:
        return int(self.quads == 4)

    def _get_nine_gates_last_tile(self) -> TileValue | None:
        if not self.no_calls():
            return None
        if not self.full_flush():
            return None
        suit = (self.hand_tiles[0] // 10) * 10
        model_tiles = [
            suit + 1,
            suit + 1,
            suit + 1,
            suit + 2,
            suit + 3,
            suit + 4,
            suit + 5,
            suit + 6,
            suit + 7,
            suit + 8,
            suit + 9,
            suit + 9,
            suit + 9,
        ]
        tile_counter = Counter(self.hand_tiles)
        tile_counter.subtract(model_tiles)
        if len(-tile_counter) > 0:
            return None
        return next(tile_counter.elements())

    @register_pattern(
        "NINE_GATES",
        display_name="Nine Gates",
        han=11,
        fu=0,
    )
    def nine_gates(self: PatternCalculator) -> int:
        nine_gates_last_tile = self._get_nine_gates_last_tile()
        return int(
            nine_gates_last_tile is not None
            and nine_gates_last_tile != self.winning_tile
        )

    @register_pattern(
        "TRUE_NINE_GATES",
        display_name="True Nine Gates",
        han=19,
        fu=0,
    )
    def true_nine_gates(self: PatternCalculator) -> int:
        nine_gates_last_tile = self._get_nine_gates_last_tile()
        return int(nine_gates_last_tile == self.winning_tile)

    @register_pattern(
        "RIICHI",
        display_name="Riichi",
        han=1,
        fu=0,
    )
    def riichi(self: PatternCalculator) -> int:
        return int(self.win.is_riichi and not self.win.is_double_riichi)

    @register_pattern(
        "DOUBLE_RIICHI",
        display_name="Double Riichi",
        han=2,
        fu=0,
    )
    def double_riichi(self: PatternCalculator) -> int:
        return int(self.win.is_double_riichi)

    @register_pattern(
        "IPPATSU",
        display_name="Ippatsu",
        han=1,
        fu=0,
    )
    def ippatsu(self: PatternCalculator) -> int:
        return int(self.win.is_ippatsu)

    @register_pattern(
        "ALL_RUNS",
        display_name="All Runs",
        han=1,
        fu=0,
    )
    def all_runs(self: PatternCalculator) -> int:
        return int(sum(self.chii_start_tiles.values()) == 4)

    @register_pattern(
        "ALL_SIMPLES",
        display_name="All Simples",
        han=1,
        fu=0,
    )
    def all_simples(self: PatternCalculator) -> int:
        return int(
            all((is_number(tile) and 2 <= tile % 10 <= 8) for tile in self.hand_tiles)
        )

    @register_pattern(
        "PURE_STRAIGHT",
        display_name="Pure Straight",
        han=3,
        fu=0,
    )
    def pure_straight(self: PatternCalculator) -> int:
        return int(
            any(
                {suit + 1, suit + 4, suit + 7} <= self.chii_start_tiles.keys()
                for suit in self._number_suits
            )
        )

    @register_pattern(
        "ALL_TRIPLETS",
        display_name="All Triplets",
        han=3,
        fu=0,
    )
    def all_triplets(self: PatternCalculator) -> int:
        return int(len(self.triplet_tiles) == 4)

    @register_pattern(
        "HALF_FLUSH",
        display_name="Half Flush",
        han=3,
        fu=0,
    )
    def half_flush(self: PatternCalculator) -> int:
        return int(len(self.used_suits) == 2 and self._honour_suit in self.used_suits)

    @register_pattern(
        "FULL_FLUSH",
        display_name="Full Flush",
        han=7,
        fu=0,
    )
    def full_flush(self: PatternCalculator) -> int:
        return int(any(self.used_suits == {suit} for suit in self._number_suits))

    @register_pattern(
        "SEVEN_PAIRS",
        display_name="Seven Pairs",
        han=3,
        fu=0,
    )
    def sevenpairs(self: PatternCalculator) -> int:
        return int(self.pair_count == 7)

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

    @register_pattern(
        "HALF_OUTSIDE_HAND",
        display_name="Half Outside Hand",
        han=2,
        fu=0,
    )
    def half_outside_hand(self: PatternCalculator) -> int:
        return int(self.call_outsidenesses == {1, 2})

    @register_pattern(
        "FULLY_OUTSIDE_HAND",
        display_name="Fully Outside Hand",
        han=4,
        fu=0,
    )
    def fully_outside_hand(self: PatternCalculator) -> int:
        return int(self.call_outsidenesses == {2})

    @register_pattern(
        "PURE_DOUBLE_SEQUENCE",
        display_name="Pure Double Sequence",
        han=1,
        fu=0,
    )
    def pure_double_sequence(self: PatternCalculator) -> int:
        return int(sum(count == 2 for count in self.chii_start_tiles.values()) == 1)

    @register_pattern(
        "TWICE_PURE_DOUBLE_SEQUENCE",
        display_name="Twice Pure Double Sequence",
        han=4,
        fu=0,
    )
    def twice_pure_double_sequence(self: PatternCalculator) -> int:
        return int(sum(count == 2 for count in self.chii_start_tiles.values()) == 2)

    @register_pattern(
        "PURE_TRIPLE_SEQUENCE",
        display_name="Pure Triple Sequence",
        han=6,
        fu=0,
    )
    def pure_triple_sequence(self: PatternCalculator) -> int:
        return int(sum(count == 3 for count in self.chii_start_tiles.values()) == 1)

    @register_pattern(
        "PURE_QUADRUPLE_SEQUENCE",
        display_name="Pure Quadruple Sequence",
        han=12,
        fu=0,
    )
    def pure_quadruple_sequence(self: PatternCalculator) -> int:
        return int(sum(count == 4 for count in self.chii_start_tiles.values()) == 1)

    @register_pattern(
        "MIXED_TRIPLE_SEQUENCE",
        display_name="Mixed Triple Sequence",
        han=2,
        fu=0,
    )
    def mixed_triple_sequence(self: PatternCalculator) -> int:
        return int(
            any(
                {tile, tile + 10, tile + 20} <= self.chii_start_tiles.keys()
                for tile in self.chii_start_tiles
                if tile < 10
            )
        )

    @register_pattern(
        "THREE_CONCEALED_TRIPLETS",
        display_name="Three Concealed Triplets",
        han=3,
        fu=0,
    )
    def three_concealed_triplets(self: PatternCalculator) -> int:
        return int(self.concealed_triplets == 3)

    @register_pattern(
        "THREE_QUADS",
        display_name="Three Quads",
        han=4,
        fu=0,
    )
    def three_quads(self: PatternCalculator) -> int:
        return int(self.quads == 3)

    @register_pattern(
        "TRIPLE_TRIPLETS",
        display_name="Triple Triplets",
        han=4,
        fu=0,
    )
    def triple_triplets(self: PatternCalculator) -> int:
        return int(
            any(
                {tile, tile + 10, tile + 20} <= self.triplet_tiles
                for tile in self.triplet_tiles
                if tile < 10
            )
        )

    @register_pattern(
        "ALL_TERMINALS_AND_HONOURS",
        display_name="All Terminals and Honours",
        han=3,
        fu=0,
    )
    def all_terminals_and_honours(self: PatternCalculator) -> int:
        return int(
            len(self.chii_start_tiles) == 0
            and self.half_outside_hand()
            and not self.thirteen_orphans()
        )

    @register_pattern(
        "EYES",
        display_name="Eyes",
        han=1,
        fu=0,
    )
    def eyes(self: PatternCalculator) -> int:
        if self.pair_count != 1:
            return 0
        tile = self.pair_tile
        if not is_number(tile):
            return 0
        return int((tile % 10) % 3 == 2)

    @register_pattern(
        "NO_CALLS",
        display_name="No Calls",
        han=1,
        fu=0,
    )
    def no_calls(self: PatternCalculator) -> int:
        return int(
            self.pair_count == 1
            and all(call.call_type == CallType.CLOSED_KAN for call in self.win.calls)
        )

    @register_pattern(
        "NO_CALLS_TSUMO",
        display_name="No Calls Tsumo",
        han=0,
        fu=0,
    )
    def no_calls_tsumo(self: PatternCalculator) -> int:
        return int(
            self.win.lose_player is None
            and all(call.call_type == CallType.CLOSED_KAN for call in self.win.calls)
        )

    @register_pattern(
        "ROBBING_A_KAN",
        display_name="Robbing a Kan",
        han=1,
        fu=0,
    )
    def robbing_a_kan(self: PatternCalculator) -> int:
        return int(self.win.is_chankan)

    @register_pattern(
        "UNDER_THE_SEA",
        display_name="Under the Sea",
        han=1,
        fu=0,
    )
    def under_the_sea(self: PatternCalculator) -> int:
        return int(self.win.is_haitei)

    @register_pattern(
        "UNDER_THE_RIVER",
        display_name="Under the River",
        han=1,
        fu=0,
    )
    def under_the_river(self: PatternCalculator) -> int:
        return int(self.win.is_houtei)

    @register_pattern(
        "AFTER_A_FLOWER",
        display_name="After a Flower",
        han=1,
        fu=0,
    )
    def after_a_flower(self: PatternCalculator) -> int:
        return self.win.after_flower_count

    @register_pattern(
        "AFTER_A_KAN",
        display_name="After a Kan",
        han=2,
        fu=0,
    )
    def after_a_kan(self: PatternCalculator) -> int:
        return self.win.after_kan_count

    @register_pattern(
        "NO_FLOWERS",
        display_name="No Flowers",
        han=1,
        fu=0,
    )
    def no_flowers(self: PatternCalculator) -> int:
        return int(len(self.flowers) == 0)

    @register_pattern(
        "SEAT_FLOWER",
        display_name="Seat Flower",
        han=1,
        fu=0,
    )
    def player_flower(self: PatternCalculator) -> int:
        return sum((tile - 41) % 4 == self.seat for tile in self.flowers)

    @register_pattern(
        "SET_OF_FLOWERS",
        display_name="Set of Flowers",
        han=2,
        fu=0,
    )
    def set_of_flowers(self: PatternCalculator) -> int:
        if self.win.player_count == 3:
            return int(
                (({41, 42, 43} <= self.flowers) + ({45, 46, 47} <= self.flowers)) == 1
            )
        else:
            return int(
                (
                    ({41, 42, 43, 44} <= self.flowers)
                    + ({45, 46, 47, 48} <= self.flowers)
                )
                == 1
            )

    @register_pattern(
        "FIVE_FLOWERS",
        display_name="Five Flowers",
        han=2,
        fu=0,
    )
    def five_flowers(self: PatternCalculator) -> int:
        return int(self.win.player_count == 3 and len(self.flowers) == 5)

    @register_pattern(
        "SEVEN_FLOWERS",
        display_name="Seven Flowers",
        han=2,
        fu=0,
    )
    def seven_flowers(self: PatternCalculator) -> int:
        return int(len(self.flowers) == 7)

    @register_pattern(
        "TWO_SETS_OF_FLOWERS",
        display_name="Two Sets of Flowers",
        han=8,
        fu=0,
    )
    def two_sets_of_flowers(self: PatternCalculator) -> int:
        if self.win.player_count == 3:
            return int(len(self.flowers) == 6)
        else:
            return int(len(self.flowers) == 8)

    @register_pattern(
        "DRAW",
        display_name="Draw",
        han=1,
        fu=0,
    )
    def draw(self: PatternCalculator) -> int:
        return self.win.draw_count

    @register_pattern(
        "NO_CALLS_RON",
        display_name="No Calls Ron",
        han=0,
        fu=10,
    )
    def ron(self: PatternCalculator) -> int:
        return int(
            self.win.lose_player is not None
            and all(call.call_type == CallType.CLOSED_KAN for call in self.win.calls)
            and not self.pair_count == 7
        )
