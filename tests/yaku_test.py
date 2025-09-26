from typing import Optional

from unittest import TestCase

from src.mahjong.tile import Tile
from src.mahjong.call import Call, CallType
from src.mahjong.yaku import Win
from src.mahjong.yaku import YakuCalculator


def get_yaku_mults(
    *,
    win_player: int = 0,
    lose_player: Optional[int],
    formed_hand: list[Call],
    calls: list[Call],
    flowers: list[Tile],
    player_count: int = 4,
    wind_round: int = 0,
    sub_round: int = 0,
    **kwargs
):
    win = Win(
        win_player=win_player,
        lose_player=lose_player,
        hand=[tile for call in formed_hand for tile in call.tiles],
        calls=calls,
        flowers=flowers,
        player_count=player_count,
        wind_round=wind_round,
        sub_round=sub_round,
        **kwargs
    )
    return YakuCalculator(win, formed_hand).get_yaku_mults()


class YakuTest(TestCase):
    def test_no_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[],
        )
        self.assertDictEqual(yaku_mults, {"NO_FLOWERS": 1})

    def test_player_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164],
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1})

    def test_sub_round_player_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[176],
            sub_round=1,
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1})

    def test_two_player_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164, 180],
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 2})

    def test_set_of_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164, 168, 172, 176],
        )
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1})

    def test_seven_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164, 168, 172, 176, 184, 188, 192],
        )
        self.assertDictEqual(
            yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1, "SEVEN_FLOWERS": 1}
        )

    def test_two_sets_of_flowers(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164, 168, 172, 176, 180, 184, 188, 192],
        )
        self.assertDictEqual(
            yaku_mults,
            {"SEAT_FLOWER": 2, "TWO_SETS_OF_FLOWERS": 1},
        )

    def test_draw(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
            draw_count=1,
        )
        self.assertDictEqual(
            yaku_mults,
            {"DRAW": 1},
        )

    def test_after_a_flower(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[128, 129, 130]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[176],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[128, 129, 130]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[176],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[124, 125, 126]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[176],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[140, 141, 142]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[144, 145, 146]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[148, 149, 150]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[32, 33]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"EYES": 1})

    def test_no_calls(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            calls=[
                Call(call_type=CallType.CLOSED_KAN, tiles=[76, 77, 78, 79]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1})

    def test_no_calls_closed_kan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            calls=[
                Call(call_type=CallType.CLOSED_KAN, tiles=[76, 77, 78, 79]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1})

    def test_chankan(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
            is_chankan=True,
        )
        self.assertDictEqual(yaku_mults, {"ROBBING_A_KAN": 1})

    def test_haitei(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
            is_haitei=True,
        )
        self.assertDictEqual(yaku_mults, {"UNDER_THE_SEA": 1})

    def test_houtei(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
            is_houtei=True,
        )
        self.assertDictEqual(yaku_mults, {"UNDER_THE_RIVER": 1})

    def test_all_runs(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[4, 5]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[6, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[56, 60, 64]),
                Call(call_type=CallType.CHI, tiles=[61, 65, 68]),
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"ALL_RUNS": 1})

    def test_all_simples(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[12, 13, 14]),
                Call(call_type=CallType.CHI, tiles=[16, 20, 24]),
                Call(call_type=CallType.PAIR, tiles=[92, 93]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[60, 61, 62]),
                Call(call_type=CallType.CHI, tiles=[63, 64, 68]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"ALL_SIMPLES": 1})

    def test_pure_straight(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[84, 88, 92]),
                Call(call_type=CallType.CHI, tiles=[96, 100, 104]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[108, 112, 116]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"PURE_STRAIGHT": 1})

    def test_all_triplets(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[4, 5, 6]),
                Call(call_type=CallType.PON, tiles=[60, 61, 62]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[92, 93, 94]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"ALL_TRIPLETS": 1})

    def test_half_flush(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[20, 24, 28]),
                Call(call_type=CallType.PON, tiles=[36, 37, 38]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[13, 16, 21]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"HALF_FLUSH": 1})

    def test_full_flush(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[20, 24, 28]),
                Call(call_type=CallType.PON, tiles=[36, 37, 38]),
                Call(call_type=CallType.PAIR, tiles=[13, 14]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[15, 16, 21]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"FULL_FLUSH": 1})

    def test_seven_pairs(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[12, 13]),
                Call(call_type=CallType.PAIR, tiles=[16, 17]),
                Call(call_type=CallType.PAIR, tiles=[36, 37]),
                Call(call_type=CallType.PAIR, tiles=[60, 61]),
                Call(call_type=CallType.PAIR, tiles=[84, 85]),
                Call(call_type=CallType.PAIR, tiles=[88, 89]),
                Call(call_type=CallType.PAIR, tiles=[124, 125]),
            ],
            calls=[],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"SEVEN_PAIRS": 1})

    def test_half_outside_hand(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[44, 48, 52]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[108, 112, 116]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[44, 48, 52]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[116, 117]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[108, 112, 118]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[5, 9, 13]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[5, 9, 13]),
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[93, 97, 101]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[12, 16, 20]),
                Call(call_type=CallType.CHI, tiles=[52, 56, 60]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.PON, tiles=[36, 37, 38]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[116, 117, 118]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.PON, tiles=[4, 5, 6]),
                Call(call_type=CallType.PON, tiles=[44, 45, 46]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[116, 117, 118]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(
            yaku_mults,
            {"HALF_OUTSIDE_HAND": 1, "ALL_TRIPLETS": 1, "ALL_TERMINALS_AND_HONOURS": 1},
        )
