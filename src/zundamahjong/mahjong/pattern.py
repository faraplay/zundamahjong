from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from typing import final
from enum import IntEnum
from typing import Optional

from .call import CallType, get_call_tiles, get_meld_type
from .meld import Meld, MeldType, TileValueMeld
from pydantic import BaseModel

from .tile import (
    TileValue,
    dragons,
    get_tile_value,
    green_tiles,
    is_number,
    orphans,
    terminals,
    winds,
)
from .win import Win


class PatternData(BaseModel):
    display_name: str
    han: int
    fu: int


default_pattern_data: dict[str, PatternData] = {}
pattern_mult_funcs: dict[str, Callable[[PatternCalculator], int]] = {}


def _register_pattern(
    name: str, display_name: str, han: int, fu: int
) -> Callable[[Callable[[PatternCalculator], int]], Callable[[PatternCalculator], int]]:
    default_pattern_data[name] = PatternData(display_name=display_name, han=han, fu=fu)

    def _register_pattern_inner(
        func: Callable[[PatternCalculator], int],
    ) -> Callable[[PatternCalculator], int]:
        pattern_mult_funcs[name] = func
        return func

    return _register_pattern_inner


class WaitPattern(IntEnum):
    RYANMEN = 0
    KANCHAN = 1
    PENCHAN = 2
    SHANPON = 3
    TANKI = 4
    KOKUSHI = 5
    KOKUSHI_13 = 6


def _get_wait_pattern(meld: TileValueMeld) -> WaitPattern:
    assert meld.winning_tile_index is not None
    meld_type = meld.meld_type
    if meld_type == MeldType.CHI:
        if meld.winning_tile_index == 0:
            if meld.tiles[0] % 10 == 7:
                return WaitPattern.PENCHAN
            else:
                return WaitPattern.RYANMEN
        elif meld.winning_tile_index == 1:
            return WaitPattern.KANCHAN
        elif meld.winning_tile_index == 2:
            if meld.tiles[2] % 10 == 3:
                return WaitPattern.PENCHAN
            else:
                return WaitPattern.RYANMEN
        else:
            raise Exception(
                f"Unexpected winning tile index {meld.winning_tile_index} in chi meld!"
            )
    elif meld_type == MeldType.PON:
        return WaitPattern.SHANPON
    elif meld_type == MeldType.PAIR:
        return WaitPattern.TANKI
    elif meld_type == MeldType.THIRTEEN_ORPHANS:
        if meld.tiles.count(meld.tiles[meld.winning_tile_index]) == 2:
            return WaitPattern.KOKUSHI_13
        else:
            return WaitPattern.KOKUSHI
    elif meld_type == MeldType.KAN:
        raise Exception("Winning tile found in kan meld!")
    else:
        raise Exception("Unknown meld type!")


@final
class PatternCalculator:
    def __init__(self, win: Win, formed_hand: list[Meld]) -> None:
        self._win = win
        self._formed_hand = formed_hand

        self._seat = (
            self._win.win_player - self._win.sub_round
        ) % self._win.player_count
        self._flowers = set(get_tile_value(flower) for flower in self._win.flowers)
        self._melds = [
            TileValueMeld(
                meld_type=meld.meld_type,
                tiles=[get_tile_value(tile) for tile in meld.tiles],
                winning_tile_index=meld.winning_tile_index,
            )
            for meld in self._formed_hand
        ] + [
            TileValueMeld(
                meld_type=get_meld_type(call.call_type),
                tiles=[get_tile_value(tile) for tile in get_call_tiles(call)],
                winning_tile_index=None,
            )
            for call in self._win.calls
        ]
        winning_meld = next(
            meld for meld in self._melds if meld.winning_tile_index is not None
        )
        assert winning_meld.winning_tile_index is not None
        self._winning_tile = winning_meld.tiles[winning_meld.winning_tile_index]
        self._wait_pattern = _get_wait_pattern(winning_meld)
        self._hand_tiles = [tile for call in self._melds for tile in call.tiles]
        self._used_suits = set((tile // 10) * 10 for tile in self._hand_tiles)
        self._call_outsidenesses = set(
            self._is_outside_call(meld) for meld in self._melds
        )
        self._chi_start_tiles = Counter(
            call.tiles[0] for call in self._melds if call.meld_type == MeldType.CHI
        )
        self._concealed_triplets = sum(
            tile_meld.meld_type == MeldType.PON
            and (tile_meld.winning_tile_index is None or self._win.lose_player is None)
            for tile_meld in self._formed_hand
        ) + sum(call.call_type == CallType.CLOSED_KAN for call in self._win.calls)
        self._quads = sum(call.meld_type == MeldType.KAN for call in self._melds)
        self._triplet_tiles = {
            call.tiles[0]
            for call in self._melds
            if call.meld_type in self._triplet_types
        }

        self._pair_count = 0
        self._pair_tile = 0
        self._chii_meld_count = 0
        self._simple_open_triplet_count = 0
        self._orphan_open_triplet_count = 0
        self._simple_closed_triplet_count = 0
        self._orphan_closed_triplet_count = 0
        self._simple_open_quad_count = 0
        self._orphan_open_quad_count = 0
        self._simple_closed_quad_count = 0
        self._orphan_closed_quad_count = 0
        for meld in self._formed_hand:
            if meld.meld_type == MeldType.CHI:
                self._chii_meld_count += 1
            elif meld.meld_type == MeldType.PON:
                if (
                    meld.winning_tile_index is not None
                    and self._win.lose_player is not None
                ):
                    if get_tile_value(meld.tiles[0]) not in orphans:
                        self._simple_open_triplet_count += 1
                    else:
                        self._orphan_open_triplet_count += 1
                else:
                    if get_tile_value(meld.tiles[0]) not in orphans:
                        self._simple_closed_triplet_count += 1
                    else:
                        self._orphan_closed_triplet_count += 1
            elif meld.meld_type == MeldType.KAN:
                raise Exception("Unexpected kan meld in formed hand!")
            elif meld.meld_type == MeldType.PAIR:
                self._pair_count += 1
                self._pair_tile = get_tile_value(meld.tiles[0])

        for call in self._win.calls:
            if call.call_type == CallType.CHI:
                self._chii_meld_count += 1
            elif call.call_type == CallType.PON:
                if get_tile_value(call.called_tile) not in orphans:
                    self._simple_open_triplet_count += 1
                else:
                    self._orphan_open_triplet_count += 1
            elif (
                call.call_type == CallType.OPEN_KAN
                or call.call_type == CallType.ADD_KAN
            ):
                if get_tile_value(call.called_tile) not in orphans:
                    self._simple_open_quad_count += 1
                else:
                    self._orphan_open_quad_count += 1
            elif call.call_type == CallType.CLOSED_KAN:
                if get_tile_value(call.tiles[0]) not in orphans:
                    self._simple_closed_quad_count += 1
                else:
                    self._orphan_closed_quad_count += 1

    _triplet_types = {MeldType.PON, MeldType.KAN}
    _number_suits = [0, 10, 20]
    _honour_suit = 30

    def get_pattern_mults(self) -> dict[str, int]:
        pattern_mults: dict[str, int] = {}
        for pattern, get_pattern_multiplicity in pattern_mult_funcs.items():
            pattern_mult = get_pattern_multiplicity(self)
            if pattern_mult != 0:
                pattern_mults[pattern] = pattern_mult
        return pattern_mults

    @_register_pattern(
        "BLESSING_OF_HEAVEN",
        display_name="Blessing of Heaven",
        han=20,
        fu=0,
    )
    def _blessing_of_heaven(self) -> int:
        return int(self._win.is_tenhou)

    @_register_pattern(
        "BLESSING_OF_EARTH",
        display_name="Blessing of Earth",
        han=19,
        fu=0,
    )
    def _blessing_of_earth(self) -> int:
        return int(self._win.is_chiihou)

    @_register_pattern(
        "LITTLE_THREE_DRAGONS",
        display_name="Little Three Dragons",
        han=5,
        fu=0,
    )
    def _little_three_dragons(self) -> int:
        total = 0
        for tile in dragons:
            tile_count = self._hand_tiles.count(tile)
            if tile_count == 4:
                tile_count = 3
            total += tile_count
        return int(total == 8)

    @_register_pattern(
        "BIG_THREE_DRAGONS",
        display_name="Big Three Dragons",
        han=8,
        fu=0,
    )
    def _big_three_dragons(self) -> int:
        return dragons <= self._triplet_tiles

    @_register_pattern(
        "FOUR_LITTLE_WINDS",
        display_name="Four Little Winds",
        han=12,
        fu=0,
    )
    def _four_little_winds(self) -> int:
        total = 0
        for tile in winds:
            tile_count = self._hand_tiles.count(tile)
            if tile_count == 4:
                tile_count = 3
            total += tile_count
        return int(total == 11)

    @_register_pattern(
        "FOUR_BIG_WINDS",
        display_name="Four Big Winds",
        han=16,
        fu=0,
    )
    def _four_big_winds(self) -> int:
        return int(winds <= self._triplet_tiles)

    @_register_pattern(
        "FOUR_CONCEALED_TRIPLETS",
        display_name="Four Concealed Triplets",
        han=12,
        fu=0,
    )
    def _four_concealed_triplets(self) -> int:
        return int(
            self._concealed_triplets == 4 and self._wait_pattern == WaitPattern.SHANPON
        )

    @_register_pattern(
        "FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT",
        display_name="Four Concealed Triplets 1-sided Wait",
        han=12,
        fu=0,
    )
    def _four_concealed_triplets_1_sided_wait(self) -> int:
        return int(
            self._concealed_triplets == 4 and self._wait_pattern == WaitPattern.TANKI
        )

    @_register_pattern(
        "ALL_HONOURS",
        display_name="All Honours",
        han=10,
        fu=0,
    )
    def _all_honours(self) -> int:
        return int(self._used_suits == {self._honour_suit})

    @_register_pattern(
        "ALL_GREENS",
        display_name="All Greens",
        han=16,
        fu=0,
    )
    def _all_greens(self) -> int:
        return int(all(tile in green_tiles for tile in self._hand_tiles))

    @_register_pattern(
        "ALL_TERMINALS",
        display_name="All Terminals",
        han=13,
        fu=0,
    )
    def _all_terminals(self) -> int:
        return int(all(tile in terminals for tile in self._hand_tiles))

    @_register_pattern(
        "THIRTEEN_ORPHANS",
        display_name="Thirteen Orphans",
        han=13,
        fu=0,
    )
    def _thirteen_orphans(self) -> int:
        return int(self._wait_pattern == WaitPattern.KOKUSHI)

    @_register_pattern(
        "THIRTEEN_ORPHANS_13_SIDED_WAIT",
        display_name="Thirteen Orphans 13-sided Wait",
        han=13,
        fu=0,
    )
    def _thirteen_orphans_13_sided_wait(self) -> int:
        return int(self._wait_pattern == WaitPattern.KOKUSHI_13)

    @_register_pattern(
        "FOUR_QUADS",
        display_name="Four Quads",
        han=18,
        fu=0,
    )
    def _four_quads(self) -> int:
        return int(self._quads == 4)

    def _get_nine_gates_last_tile(self) -> Optional[TileValue]:
        if not self._no_calls():
            return None
        if not self._full_flush():
            return None
        suit = (self._hand_tiles[0] // 10) * 10
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
        tile_counter = Counter(self._hand_tiles)
        tile_counter.subtract(model_tiles)
        if len(-tile_counter) > 0:
            return None
        return next(tile_counter.elements())

    @_register_pattern(
        "NINE_GATES",
        display_name="Nine Gates",
        han=11,
        fu=0,
    )
    def _nine_gates(self) -> int:
        nine_gates_last_tile = self._get_nine_gates_last_tile()
        return int(
            nine_gates_last_tile is not None
            and nine_gates_last_tile != self._winning_tile
        )

    @_register_pattern(
        "TRUE_NINE_GATES",
        display_name="True Nine Gates",
        han=19,
        fu=0,
    )
    def _true_nine_gates(self) -> int:
        nine_gates_last_tile = self._get_nine_gates_last_tile()
        return int(nine_gates_last_tile == self._winning_tile)

    @_register_pattern(
        "ALL_RUNS",
        display_name="All Runs",
        han=1,
        fu=0,
    )
    def _all_runs(self) -> int:
        return int(sum(self._chi_start_tiles.values()) == 4)

    @_register_pattern(
        "ALL_SIMPLES",
        display_name="All Simples",
        han=1,
        fu=0,
    )
    def _all_simples(self) -> int:
        return int(
            all((is_number(tile) and 2 <= tile % 10 <= 8) for tile in self._hand_tiles)
        )

    @_register_pattern(
        "PURE_STRAIGHT",
        display_name="Pure Straight",
        han=3,
        fu=0,
    )
    def _pure_straight(self) -> int:
        return int(
            any(
                {suit + 1, suit + 4, suit + 7} <= self._chi_start_tiles.keys()
                for suit in self._number_suits
            )
        )

    @_register_pattern(
        "ALL_TRIPLETS",
        display_name="All Triplets",
        han=3,
        fu=0,
    )
    def _all_triplets(self) -> int:
        return int(len(self._triplet_tiles) == 4)

    @_register_pattern(
        "HALF_FLUSH",
        display_name="Half Flush",
        han=3,
        fu=0,
    )
    def _half_flush(self) -> int:
        return int(len(self._used_suits) == 2 and self._honour_suit in self._used_suits)

    @_register_pattern(
        "FULL_FLUSH",
        display_name="Full Flush",
        han=7,
        fu=0,
    )
    def _full_flush(self) -> int:
        return int(any(self._used_suits == {suit} for suit in self._number_suits))

    @_register_pattern(
        "SEVEN_PAIRS",
        display_name="Seven Pairs",
        han=3,
        fu=0,
    )
    def _seven_pairs(self) -> int:
        return int(self._pair_count == 7)

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

    @_register_pattern(
        "HALF_OUTSIDE_HAND",
        display_name="Half Outside Hand",
        han=2,
        fu=0,
    )
    def _half_outside_hand(self) -> int:
        return int(self._call_outsidenesses == {1, 2})

    @_register_pattern(
        "FULLY_OUTSIDE_HAND",
        display_name="Fully Outside Hand",
        han=4,
        fu=0,
    )
    def _fully_outside_hand(self) -> int:
        return int(self._call_outsidenesses == {2})

    @_register_pattern(
        "PURE_DOUBLE_SEQUENCE",
        display_name="Pure Double Sequence",
        han=1,
        fu=0,
    )
    def _pure_double_sequence(self) -> int:
        return int(sum(count == 2 for count in self._chi_start_tiles.values()) == 1)

    @_register_pattern(
        "TWICE_PURE_DOUBLE_SEQUENCE",
        display_name="Twice Pure Double Sequence",
        han=4,
        fu=0,
    )
    def _twice_pure_double_sequence(self) -> int:
        return int(sum(count == 2 for count in self._chi_start_tiles.values()) == 2)

    @_register_pattern(
        "PURE_TRIPLE_SEQUENCE",
        display_name="Pure Triple Sequence",
        han=6,
        fu=0,
    )
    def _pure_triple_sequence(self) -> int:
        return int(sum(count == 3 for count in self._chi_start_tiles.values()) == 1)

    @_register_pattern(
        "PURE_QUADRUPLE_SEQUENCE",
        display_name="Pure Quadruple Sequence",
        han=12,
        fu=0,
    )
    def _pure_quadruple_sequence(self) -> int:
        return int(sum(count == 4 for count in self._chi_start_tiles.values()) == 1)

    @_register_pattern(
        "MIXED_TRIPLE_SEQUENCE",
        display_name="Mixed Triple Sequence",
        han=2,
        fu=0,
    )
    def _mixed_triple_sequence(self) -> int:
        return int(
            any(
                {tile, tile + 10, tile + 20} <= self._chi_start_tiles.keys()
                for tile in self._chi_start_tiles
                if tile < 10
            )
        )

    @_register_pattern(
        "THREE_CONCEALED_TRIPLETS",
        display_name="Three Concealed Triplets",
        han=3,
        fu=0,
    )
    def _three_concealed_triplets(self) -> int:
        return int(self._concealed_triplets == 3)

    @_register_pattern(
        "THREE_QUADS",
        display_name="Three Quads",
        han=4,
        fu=0,
    )
    def _three_quads(self) -> int:
        return int(self._quads == 3)

    @_register_pattern(
        "TRIPLE_TRIPLETS",
        display_name="Triple Triplets",
        han=4,
        fu=0,
    )
    def _triple_triplets(self) -> int:
        return int(
            any(
                {tile, tile + 10, tile + 20} <= self._triplet_tiles
                for tile in self._triplet_tiles
                if tile < 10
            )
        )

    @_register_pattern(
        "ALL_TERMINALS_AND_HONOURS",
        display_name="All Terminals and Honours",
        han=3,
        fu=0,
    )
    def _all_terminals_and_honours(self) -> int:
        return int(
            len(self._chi_start_tiles) == 0
            and self._half_outside_hand()
            and not self._thirteen_orphans()
        )

    def _yakuhai(self, pattern_tile: TileValue) -> int:
        return int(
            any(
                (call.tiles[0] == pattern_tile and call.meld_type != MeldType.PAIR)
                for call in self._melds
            )
        )

    @_register_pattern(
        "SEAT_WIND",
        display_name="Seat Wind",
        han=1,
        fu=0,
    )
    def _player_wind(self) -> int:
        return self._yakuhai(self._seat + 31)

    @_register_pattern(
        "PREVALENT_WIND",
        display_name="Prevalent Wind",
        han=1,
        fu=0,
    )
    def _prevalent_wind(self) -> int:
        return self._yakuhai(self._win.wind_round + 31)

    @_register_pattern(
        "NORTH_WIND",
        display_name="North Wind",
        han=1,
        fu=0,
    )
    def _north_wind(self) -> int:
        return int(self._win.player_count == 3 and self._yakuhai(34))

    @_register_pattern(
        "WHITE_DRAGON",
        display_name="White Dragon",
        han=1,
        fu=0,
    )
    def _white_dragon(self) -> int:
        return self._yakuhai(35)

    @_register_pattern(
        "GREEN_DRAGON",
        display_name="Green Dragon",
        han=1,
        fu=0,
    )
    def _green_dragon(self) -> int:
        return self._yakuhai(36)

    @_register_pattern(
        "RED_DRAGON",
        display_name="Red Dragon",
        han=1,
        fu=0,
    )
    def _red_dragon(self) -> int:
        return self._yakuhai(37)

    @_register_pattern(
        "EYES",
        display_name="Eyes",
        han=1,
        fu=0,
    )
    def _eyes(self) -> int:
        if self._pair_count != 1:
            return 0
        tile = self._pair_tile
        if not is_number(tile):
            return 0
        return int((tile % 10) % 3 == 2)

    @_register_pattern(
        "NO_CALLS",
        display_name="No Calls",
        han=1,
        fu=0,
    )
    def _no_calls(self) -> int:
        return int(
            self._pair_count == 1
            and all(call.call_type == CallType.CLOSED_KAN for call in self._win.calls)
        )

    @_register_pattern(
        "NO_CALLS_TSUMO",
        display_name="No Calls Tsumo",
        han=0,
        fu=0,
    )
    def _no_calls_tsumo(self) -> int:
        return int(
            self._win.lose_player is None
            and all(call.call_type == CallType.CLOSED_KAN for call in self._win.calls)
        )

    @_register_pattern(
        "ROBBING_A_KAN",
        display_name="Robbing a Kan",
        han=1,
        fu=0,
    )
    def _robbing_a_kan(self) -> int:
        return int(self._win.is_chankan)

    @_register_pattern(
        "UNDER_THE_SEA",
        display_name="Under the Sea",
        han=1,
        fu=0,
    )
    def _under_the_sea(self) -> int:
        return int(self._win.is_haitei)

    @_register_pattern(
        "UNDER_THE_RIVER",
        display_name="Under the River",
        han=1,
        fu=0,
    )
    def _under_the_river(self) -> int:
        return int(self._win.is_houtei)

    @_register_pattern(
        "AFTER_A_FLOWER",
        display_name="After a Flower",
        han=1,
        fu=0,
    )
    def _after_a_flower(self) -> int:
        return self._win.after_flower_count

    @_register_pattern(
        "AFTER_A_KAN",
        display_name="After a Kan",
        han=2,
        fu=0,
    )
    def _after_a_kan(self) -> int:
        return self._win.after_kan_count

    @_register_pattern(
        "NO_FLOWERS",
        display_name="No Flowers",
        han=1,
        fu=0,
    )
    def _no_flowers(self) -> int:
        return int(len(self._flowers) == 0)

    @_register_pattern(
        "SEAT_FLOWER",
        display_name="Seat Flower",
        han=1,
        fu=0,
    )
    def _player_flower(self) -> int:
        return sum((tile - 41) % 4 == self._seat for tile in self._flowers)

    @_register_pattern(
        "SET_OF_FLOWERS",
        display_name="Set of Flowers",
        han=2,
        fu=0,
    )
    def _set_of_flowers(self) -> int:
        if self._win.player_count == 3:
            return int(
                (({41, 42, 43} <= self._flowers) + ({45, 46, 47} <= self._flowers)) == 1
            )
        else:
            return int(
                (
                    ({41, 42, 43, 44} <= self._flowers)
                    + ({45, 46, 47, 48} <= self._flowers)
                )
                == 1
            )

    @_register_pattern(
        "FIVE_FLOWERS",
        display_name="Five Flowers",
        han=2,
        fu=0,
    )
    def _five_flowers(self) -> int:
        return int(self._win.player_count == 3 and len(self._flowers) == 5)

    @_register_pattern(
        "SEVEN_FLOWERS",
        display_name="Seven Flowers",
        han=2,
        fu=0,
    )
    def _seven_flowers(self) -> int:
        return int(len(self._flowers) == 7)

    @_register_pattern(
        "TWO_SETS_OF_FLOWERS",
        display_name="Two Sets of Flowers",
        han=8,
        fu=0,
    )
    def _two_sets_of_flowers(self) -> int:
        if self._win.player_count == 3:
            return int(len(self._flowers) == 6)
        else:
            return int(len(self._flowers) == 8)

    @_register_pattern(
        "DRAW",
        display_name="Draw",
        han=1,
        fu=0,
    )
    def _draw(self) -> int:
        return self._win.draw_count

    @_register_pattern(
        "OPEN_WAIT",
        display_name="Open Wait",
        han=0,
        fu=0,
    )
    def _open_wait(self) -> int:
        return int(self._wait_pattern == WaitPattern.RYANMEN)

    @_register_pattern(
        "CLOSED_WAIT",
        display_name="Closed Wait",
        han=0,
        fu=0,
    )
    def _closed_wait(self) -> int:
        return int(self._wait_pattern == WaitPattern.KANCHAN)

    @_register_pattern(
        "EDGE_WAIT",
        display_name="Edge Wait",
        han=0,
        fu=0,
    )
    def _edge_wait(self) -> int:
        return int(self._wait_pattern == WaitPattern.PENCHAN)

    @_register_pattern(
        "DUAL_PON_WAIT",
        display_name="Dual Pon Wait",
        han=0,
        fu=0,
    )
    def _dual_pon_wait(self) -> int:
        return int(self._wait_pattern == WaitPattern.SHANPON)

    @_register_pattern(
        "PAIR_WAIT",
        display_name="Pair Wait",
        han=0,
        fu=0,
    )
    def _pair_wait(self) -> int:
        return int(self._wait_pattern == WaitPattern.TANKI and self._pair_count == 1)

    @_register_pattern(
        "SIMPLE_OPEN_TRIPLET",
        display_name="Simple Open Triplet",
        han=0,
        fu=0,
    )
    def _simple_open_triplet(self) -> int:
        return self._simple_open_triplet_count

    @_register_pattern(
        "ORPHAN_OPEN_TRIPLET",
        display_name="Orphan Open Triplet",
        han=0,
        fu=0,
    )
    def _orphan_open_triplet(self) -> int:
        return self._orphan_open_triplet_count

    @_register_pattern(
        "SIMPLE_CLOSED_TRIPLET",
        display_name="Simple Closed Triplet",
        han=0,
        fu=0,
    )
    def _simple_closed_triplet(self) -> int:
        return self._simple_closed_triplet_count

    @_register_pattern(
        "ORPHAN_CLOSED_TRIPLET",
        display_name="Orphan Closed Triplet",
        han=0,
        fu=0,
    )
    def _orphan_closed_triplet(self) -> int:
        return self._orphan_closed_triplet_count

    @_register_pattern(
        "SIMPLE_OPEN_QUAD",
        display_name="Simple Open Quad",
        han=0,
        fu=0,
    )
    def _simple_open_quad(self) -> int:
        return self._simple_open_quad_count

    @_register_pattern(
        "ORPHAN_OPEN_QUAD",
        display_name="Orphan Open Quad",
        han=0,
        fu=0,
    )
    def _orphan_open_quad(self) -> int:
        return self._orphan_open_quad_count

    @_register_pattern(
        "SIMPLE_CLOSED_QUAD",
        display_name="Simple Closed Quad",
        han=0,
        fu=0,
    )
    def _simple_closed_quad(self) -> int:
        return self._simple_closed_quad_count

    @_register_pattern(
        "ORPHAN_CLOSED_QUAD",
        display_name="Orphan Closed Quad",
        han=0,
        fu=0,
    )
    def _orphan_closed_quad(self) -> int:
        return self._orphan_closed_quad_count

    @_register_pattern(
        "YAKUHAI_PAIR",
        display_name="Yakuhai Pair",
        han=0,
        fu=0,
    )
    def _yakuhai_pair(self) -> int:
        if self._pair_count != 1:
            return 0
        yakuhai = [
            self._seat + 31,
            self._win.wind_round + 31,
            35,
            36,
            37,
        ]
        return sum(self._pair_tile == tile for tile in yakuhai)

    @_register_pattern(
        "PINFU",
        display_name="Pinfu",
        han=0,
        fu=0,
    )
    def _pinfu(self) -> int:
        return int(
            len(self._win.calls) == 0
            and self._chii_meld_count == 4
            and self._wait_pattern == WaitPattern.RYANMEN
            and not self._yakuhai_pair()
        )

    @_register_pattern(
        "OPEN_PINFU",
        display_name="Open Pinfu",
        han=0,
        fu=0,
    )
    def _open_pinfu(self) -> int:
        return int(
            len(self._win.calls) != 0
            and self._chii_meld_count == 4
            and self._wait_pattern == WaitPattern.RYANMEN
            and not self._yakuhai_pair()
        )

    @_register_pattern(
        "CLOSED_HAND_RON",
        display_name="Closed Hand Ron",
        han=0,
        fu=0,
    )
    def _ron(self) -> int:
        return int(
            self._win.lose_player is not None
            and all(call.call_type == CallType.CLOSED_KAN for call in self._win.calls)
        )

    @_register_pattern(
        "NON_PINFU_TSUMO",
        display_name="Non Pinfu Tsumo",
        han=0,
        fu=0,
    )
    def _non_pinfu_tsumo(self) -> int:
        return int(self._win.lose_player is None and not self._pinfu())
