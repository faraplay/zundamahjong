from __future__ import annotations
from collections import Counter
from collections.abc import Callable

from .tile import (
    get_tile_value,
    is_number,
    terminals,
    winds,
    dragons,
    green_tiles,
)
from .meld import Meld, MeldType, TileValueMeld
from .call import CallType, get_call_tiles, get_meld_type
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
    def __init__(self, win: Win, formed_hand: list[Meld]):
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
            )
            for meld in self._formed_hand
        ] + [
            TileValueMeld(
                meld_type=get_meld_type(call.call_type),
                tiles=[get_tile_value(tile) for tile in get_call_tiles(call)],
            )
            for call in self._win.calls
        ]
        self._hand_tiles = [tile for call in self._melds for tile in call.tiles]
        self._used_suits = set((tile // 10) * 10 for tile in self._hand_tiles)
        self._call_outsidenesses = set(
            self._is_outside_call(meld) for meld in self._melds
        )
        self._chi_start_tiles = Counter(
            call.tiles[0] for call in self._melds if call.meld_type == MeldType.CHI
        )
        self._triplet_tiles = {
            call.tiles[0]
            for call in self._melds
            if call.meld_type in self._triplet_types
        }

    _triplet_types = {
        MeldType.PON,
        MeldType.OPEN_KAN,
        MeldType.ADD_KAN,
        MeldType.CLOSED_KAN,
    }
    _kan_types = {MeldType.OPEN_KAN, MeldType.ADD_KAN, MeldType.CLOSED_KAN}
    _number_suits = [0, 10, 20]
    _honour_suit = 30

    def get_yaku_mults(self):
        yaku_mults: dict[str, int] = {}
        for yaku, get_yaku_multiplicity in yaku_mult_funcs.items():
            yaku_mult = get_yaku_multiplicity(self)
            if yaku_mult != 0:
                yaku_mults[yaku] = yaku_mult
        return yaku_mults

    @_register_yaku("BLESSING_OF_HEAVEN", "Blessing of Heaven", 20)
    def _blessing_of_heaven(self):
        return int(self._win.is_tenhou)

    @_register_yaku("BLESSING_OF_EARTH", "Blessing of Earth", 19)
    def _blessing_of_earth(self):
        return int(self._win.is_chiihou)

    @_register_yaku("LITTLE_THREE_DRAGONS", "Little Three Dragons", 5)
    def _little_three_dragons(self):
        total = 0
        for tile in dragons:
            tile_count = self._hand_tiles.count(tile)
            if tile_count == 4:
                tile_count = 3
            total += tile_count
        return int(total == 8)

    @_register_yaku("BIG_THREE_DRAGONS", "Big Three Dragons", 8)
    def _big_three_dragons(self):
        return dragons <= self._triplet_tiles

    @_register_yaku("FOUR_LITTLE_WINDS", "Four Little Winds", 12)
    def _four_little_winds(self):
        total = 0
        for tile in winds:
            tile_count = self._hand_tiles.count(tile)
            if tile_count == 4:
                tile_count = 3
            total += tile_count
        return int(total == 11)

    @_register_yaku("FOUR_BIG_WINDS", "Four Big Winds", 16)
    def _four_big_winds(self):
        return int(winds <= self._triplet_tiles)

    @_register_yaku("FOUR_CONCEALED_TRIPLETS", "Four Concealed Triplets", 12)
    def _four_concealed_triplets(self):
        return int(self._no_calls() and self._all_triplets())

    @_register_yaku("ALL_HONOURS", "All Honours", 10)
    def _all_honours(self):
        return int(self._used_suits == {self._honour_suit})

    @_register_yaku("ALL_GREENS", "All Greens", 16)
    def _all_greens(self):
        return int(all(tile in green_tiles for tile in self._hand_tiles))

    @_register_yaku("ALL_TERMINALS", "All Terminals", 13)
    def _all_terminals(self):
        return int(all(tile in terminals for tile in self._hand_tiles))

    @_register_yaku("THIRTEEN_ORPHANS", "Thirteen Orphans", 13)
    def _thirteen_orphans(self):
        return int(self._melds[0].meld_type == MeldType.THIRTEEN_ORPHANS)

    @_register_yaku("FOUR_QUADS", "Four Quads", 18)
    def _four_quads(self):
        return int(sum(call.meld_type in self._kan_types for call in self._melds) == 4)

    @_register_yaku("NINE_GATES", "Nine Gates", 11)
    def _nine_gates(self):
        if not self._no_calls():
            return 0
        if not self._full_flush():
            return 0
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
        return int(len(-tile_counter) == 0)

    @_register_yaku("ALL_RUNS", "All Runs", 1)
    def _all_runs(self):
        return int(sum(self._chi_start_tiles.values()) == 4)

    @_register_yaku("ALL_SIMPLES", "All Simples", 1)
    def _all_simples(self):
        return int(
            all((is_number(tile) and 2 <= tile % 10 <= 8) for tile in self._hand_tiles)
        )

    @_register_yaku("PURE_STRAIGHT", "Pure Straight", 3)
    def _pure_straight(self):
        return int(
            any(
                {suit + 1, suit + 4, suit + 7} <= self._chi_start_tiles.keys()
                for suit in self._number_suits
            )
        )

    @_register_yaku("ALL_TRIPLETS", "All Triplets", 3)
    def _all_triplets(self):
        return int(len(self._triplet_tiles) == 4)

    @_register_yaku("HALF_FLUSH", "Half Flush", 3)
    def _half_flush(self):
        return int(len(self._used_suits) == 2 and self._honour_suit in self._used_suits)

    @_register_yaku("FULL_FLUSH", "Full Flush", 7)
    def _full_flush(self):
        return int(any(self._used_suits == {suit} for suit in self._number_suits))

    @_register_yaku("SEVEN_PAIRS", "Seven Pairs", 3)
    def _seven_pairs(self):
        return len(self._melds) == 7 and int(
            all(call.meld_type == MeldType.PAIR for call in self._melds)
        )

    def _is_outside_call(self, meld: TileValueMeld):
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

    @_register_yaku("HALF_OUTSIDE_HAND", "Half Outside Hand", 2)
    def _half_outside_hand(self):
        return int(self._call_outsidenesses == {1, 2})

    @_register_yaku("FULLY_OUTSIDE_HAND", "Fully Outside Hand", 4)
    def _fully_outside_hand(self):
        return int(self._call_outsidenesses == {2})

    @_register_yaku("PURE_DOUBLE_SEQUENCE", "Pure Double Sequence", 1)
    def _pure_double_sequence(self):
        return int(sum(count == 2 for count in self._chi_start_tiles.values()) == 1)

    @_register_yaku("TWICE_PURE_DOUBLE_SEQUENCE", "Twice Pure Double Sequence", 4)
    def _twice_pure_double_sequence(self):
        return int(sum(count == 2 for count in self._chi_start_tiles.values()) == 2)

    @_register_yaku("MIXED_TRIPLE_SEQUENCE", "Mixed Triple Sequence", 2)
    def _mixed_triple_sequence(self):
        return int(
            any(
                {tile, tile + 10, tile + 20} <= self._chi_start_tiles.keys()
                for tile in self._chi_start_tiles
                if tile < 10
            )
        )

    @_register_yaku("TRIPLE_TRIPLETS", "Triple Triplets", 4)
    def _triple_triplets(self):
        return int(
            any(
                {tile, tile + 10, tile + 20} <= self._triplet_tiles
                for tile in self._triplet_tiles
                if tile < 10
            )
        )

    @_register_yaku("ALL_TERMINALS_AND_HONOURS", "All Terminals and Honours", 3)
    def _all_terminals_and_honours(self):
        return int(
            len(self._chi_start_tiles) == 0
            and self._half_outside_hand()
            and not self._thirteen_orphans()
        )

    def _yakuhai(self, yaku_tile):
        return int(
            any(
                (call.tiles[0] == yaku_tile and call.meld_type != MeldType.PAIR)
                for call in self._melds
            )
        )

    @_register_yaku("SEAT_WIND", "Seat Wind", 1)
    def _player_wind(self):
        return self._yakuhai(self._seat + 31)

    @_register_yaku("PREVALENT_WIND", "Prevalent Wind", 1)
    def _prevalent_wind(self):
        return self._yakuhai(self._win.wind_round + 31)

    @_register_yaku("NORTH_WIND", "North Wind", 1)
    def _north_wind(self):
        return int(self._win.player_count == 3 and self._yakuhai(34))

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
        pairs = [call for call in self._melds if call.meld_type == MeldType.PAIR]
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
            and all(call.call_type == CallType.CLOSED_KAN for call in self._win.calls)
        )

    @_register_yaku("ROBBING_A_KAN", "Robbing a Kan", 1)
    def _robbing_a_kan(self):
        return int(self._win.is_chankan)

    @_register_yaku("UNDER_THE_SEA", "Under the Sea", 1)
    def _under_the_sea(self):
        return int(self._win.is_haitei)

    @_register_yaku("UNDER_THE_RIVER", "Under the River", 1)
    def _under_the_river(self):
        return int(self._win.is_houtei)

    @_register_yaku("AFTER_A_FLOWER", "After a Flower", 1)
    def _after_a_flower(self):
        return self._win.after_flower_count

    @_register_yaku("AFTER_A_KAN", "After a Kan", 2)
    def _after_a_kan(self):
        return self._win.after_kan_count

    @_register_yaku("NO_FLOWERS", "No Flowers", 1)
    def _no_flowers(self):
        return int(len(self._flowers) == 0)

    @_register_yaku("SEAT_FLOWER", "Seat Flower", 1)
    def _player_flower(self):
        return sum((tile - 41) % 4 == self._seat for tile in self._flowers)

    @_register_yaku("SET_OF_FLOWERS", "Set of Flowers", 2)
    def _set_of_flowers(self):
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

    @_register_yaku("FIVE_FLOWERS", "Five Flowers", 2)
    def _five_flowers(self):
        return int(self._win.player_count == 3 and len(self._flowers) == 5)

    @_register_yaku("SEVEN_FLOWERS", "Seven Flowers", 2)
    def _seven_flowers(self):
        return int(len(self._flowers) == 7)

    @_register_yaku("TWO_SETS_OF_FLOWERS", "Two Sets of Flowers", 8)
    def _two_sets_of_flowers(self):
        if self._win.player_count == 3:
            return int(len(self._flowers) == 6)
        else:
            return int(len(self._flowers) == 8)

    @_register_yaku("DRAW", "Draw", 1)
    def _draw(self):
        return self._win.draw_count
