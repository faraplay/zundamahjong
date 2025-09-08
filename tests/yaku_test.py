from unittest import TestCase

from src.mahjong.call import Call, CallType
from src.mahjong.yaku import Win
from src.mahjong.yaku import YakuCalculator


def get_yaku_mults(
    *,
    win_player: int = 0,
    lose_player: int | None = None,
    formed_hand: list[Call],
    calls: list[Call],
    wind_round: int = 0,
    **kwargs
):
    win = Win(
        win_player=win_player,
        lose_player=lose_player,
        hand=[tile for call in formed_hand for tile in call.tiles],
        calls=calls,
        wind_round=wind_round,
        **kwargs
    )
    return YakuCalculator(win, formed_hand).get_yaku_mults()


class YakuTest(TestCase):
    def test_no_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"NO_FLOWERS": 1})

    def test_player_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[41]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1})

    def test_sub_round_player_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
            ],
            sub_round=1,
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1})

    def test_two_player_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[45]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 2})

    def test_set_of_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
                Call(call_type=CallType.FLOWER, tiles=[43]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1})

    def test_seven_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
                Call(call_type=CallType.FLOWER, tiles=[43]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
                Call(call_type=CallType.FLOWER, tiles=[46]),
                Call(call_type=CallType.FLOWER, tiles=[47]),
                Call(call_type=CallType.FLOWER, tiles=[48]),
            ],
        )
        self.assertDictEqual(
            yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1, "SEVEN_FLOWERS": 1}
        )

    def test_two_sets_of_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
                Call(call_type=CallType.FLOWER, tiles=[43]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
                Call(call_type=CallType.FLOWER, tiles=[45]),
                Call(call_type=CallType.FLOWER, tiles=[46]),
                Call(call_type=CallType.FLOWER, tiles=[47]),
                Call(call_type=CallType.FLOWER, tiles=[48]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"SEAT_FLOWER": 2, "SET_OF_FLOWERS": 1, "TWO_SETS_OF_FLOWERS": 1},
        )

    def test_after_a_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            after_flower_count=1,
        )
        self.assertDictEqual(
            yaku_mults,
            {"AFTER_A_FLOWER": 1},
        )

    def test_after_a_kan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            after_kan_count=1,
        )
        self.assertDictEqual(
            yaku_mults,
            {"AFTER_A_KAN": 1},
        )

    def test_player_wind(self):
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[32, 32, 32]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"SEAT_WIND": 1},
        )

    def test_sub_round_player_wind(self):
        yaku_mults = get_yaku_mults(
            win_player=2,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[32, 32, 32]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
            ],
            sub_round=1,
        )
        self.assertDictEqual(
            yaku_mults,
            {"SEAT_WIND": 1},
        )

    def test_prevalent_wind(self):
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[31, 31, 31]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"PREVALENT_WIND": 1},
        )

    def test_white_dragon(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[35, 35, 35]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"WHITE_DRAGON": 1},
        )

    def test_green_dragon(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[36, 36, 36]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"GREEN_DRAGON": 1},
        )

    def test_red_dragon(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[37, 37, 37]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"RED_DRAGON": 1},
        )

    def test_eyes(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[8, 8]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"EYES": 1})

    def test_no_calls(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
            ],
            calls=[
                Call(call_type=CallType.CLOSED_KAN, tiles=[19, 19, 19, 19]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1})

    def test_no_calls_closed_kan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
            ],
            calls=[
                Call(call_type=CallType.CLOSED_KAN, tiles=[19, 19, 19, 19]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1})

    def test_chankan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            is_chankan=True,
        )
        self.assertDictEqual(yaku_mults, {"ROBBING_A_KAN": 1})

    def test_haitei(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            is_haitei=True,
        )
        self.assertDictEqual(yaku_mults, {"UNDER_THE_SEA": 1})

    def test_houtei(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            is_houtei=True,
        )
        self.assertDictEqual(yaku_mults, {"UNDER_THE_RIVER": 1})

    def test_all_runs(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[1, 1]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[14, 15, 16]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"ALL_RUNS": 1})

    def test_all_simples(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[3, 3, 3]),
                Call(call_type=CallType.CHI, tiles=[4, 5, 6]),
                Call(call_type=CallType.PAIR, tiles=[23, 23]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[15, 15, 15]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"ALL_SIMPLES": 1})

    def test_pure_straight(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[21, 22, 23]),
                Call(call_type=CallType.CHI, tiles=[24, 25, 26]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[27, 28, 29]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"PURE_STRAIGHT": 1})

    def test_all_triplets(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[1, 1, 1]),
                Call(call_type=CallType.PON, tiles=[15, 15, 15]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[23, 23, 23]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"ALL_TRIPLETS": 1})

    def test_half_flush(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[5, 6, 7]),
                Call(call_type=CallType.PON, tiles=[9, 9, 9]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[3, 4, 5]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"HALF_FLUSH": 1})

    def test_full_flush(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[5, 6, 7]),
                Call(call_type=CallType.PON, tiles=[9, 9, 9]),
                Call(call_type=CallType.PAIR, tiles=[3, 3]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[3, 4, 5]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"FULL_FLUSH": 1})

    def test_seven_pairs(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[3, 3]),
                Call(call_type=CallType.PAIR, tiles=[4, 4]),
                Call(call_type=CallType.PAIR, tiles=[9, 9]),
                Call(call_type=CallType.PAIR, tiles=[15, 15]),
                Call(call_type=CallType.PAIR, tiles=[21, 21]),
                Call(call_type=CallType.PAIR, tiles=[22, 22]),
                Call(call_type=CallType.PAIR, tiles=[31, 31]),
            ],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"SEVEN_PAIRS": 1})

    def test_half_outside_hand(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[11, 12, 13]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[27, 28, 29]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"HALF_OUTSIDE_HAND": 1},
        )

    def test_fully_outside_hand(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[11, 12, 13]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[29, 29]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[27, 28, 29]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"FULLY_OUTSIDE_HAND": 1},
        )

    def test_pure_double_sequence(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"PURE_DOUBLE_SEQUENCE": 1},
        )

    def test_twice_pure_double_sequence(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"ALL_RUNS": 1, "TWICE_PURE_DOUBLE_SEQUENCE": 1},
        )

    def test_mixed_triple_sequence(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[3, 4, 5]),
                Call(call_type=CallType.CHI, tiles=[13, 14, 15]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"MIXED_TRIPLE_SEQUENCE": 1},
        )

    def test_triple_triplets(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[9, 9, 9]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[29, 29, 29]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"TRIPLE_TRIPLETS": 1},
        )

    def test_all_terminals_and_honours(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[1, 1, 1]),
                Call(call_type=CallType.PON, tiles=[11, 11, 11]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[29, 29, 29]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {"HALF_OUTSIDE_HAND": 1, "ALL_TRIPLETS": 1, "ALL_TERMINALS_AND_HONOURS": 1},
        )
