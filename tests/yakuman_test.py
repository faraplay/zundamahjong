from unittest import TestCase

from src.mahjong.call import Call, CallType
from tests.yaku_test import get_yaku_mults


class YakumanTest(TestCase):
    def test_blessing_of_heaven(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
            is_tenhou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_HEAVEN": 1})

    def test_blessing_of_earth(self):
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 17]),
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.CHI, tiles=[23, 24, 25]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[43]),
            ],
            is_chiihou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_EARTH": 1})

    def test_little_three_dragons(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.PON, tiles=[35, 35, 35]),
                Call(call_type=CallType.PON, tiles=[23, 23, 23]),
                Call(call_type=CallType.PAIR, tiles=[36, 36]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[37, 37, 37]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults, {"WHITE_DRAGON": 1, "RED_DRAGON": 1, "LITTLE_THREE_DRAGONS": 1}
        )

    def test_big_three_dragons(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.PON, tiles=[35, 35, 35]),
                Call(call_type=CallType.PON, tiles=[36, 36, 36]),
                Call(call_type=CallType.PAIR, tiles=[23, 23]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[37, 37, 37]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {
                "WHITE_DRAGON": 1,
                "GREEN_DRAGON": 1,
                "RED_DRAGON": 1,
                "BIG_THREE_DRAGONS": 1,
            },
        )

    def test_four_little_winds(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[2, 3, 4]),
                Call(call_type=CallType.PON, tiles=[33, 33, 33]),
                Call(call_type=CallType.PON, tiles=[34, 34, 34]),
                Call(call_type=CallType.PAIR, tiles=[31, 31]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[32, 32, 32]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {
                "HALF_FLUSH": 1,
                "FOUR_LITTLE_WINDS": 1,
            },
        )

    def test_four_big_winds(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[31, 31, 31]),
                Call(call_type=CallType.PON, tiles=[33, 33, 33]),
                Call(call_type=CallType.PON, tiles=[34, 34, 34]),
                Call(call_type=CallType.PAIR, tiles=[3, 3]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[32, 32, 32]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {
                "SEAT_WIND": 1,
                "PREVALENT_WIND": 1,
                "HALF_FLUSH": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_BIG_WINDS": 1,
            },
        )

    def test_four_concealed_triplets(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[1, 1, 1]),
                Call(call_type=CallType.PON, tiles=[15, 15, 15]),
                Call(call_type=CallType.PON, tiles=[23, 23, 23]),
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.CLOSED_KAN, tiles=[19, 19, 19, 19]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "ALL_TRIPLETS": 1, "FOUR_CONCEALED_TRIPLETS": 1}
        )

    def test_all_honours(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[36, 36, 36]),
                Call(call_type=CallType.PON, tiles=[33, 33, 33]),
                Call(call_type=CallType.PON, tiles=[34, 34, 34]),
                Call(call_type=CallType.PAIR, tiles=[35, 35]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[32, 32, 32]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults,
            {
                "GREEN_DRAGON": 1,
                "ALL_TRIPLETS": 1,
                "ALL_HONOURS": 1,
            },
        )

    def test_all_greens(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[22, 23, 24]),
                Call(call_type=CallType.PON, tiles=[23, 23, 23]),
                Call(call_type=CallType.CHI, tiles=[28, 28, 28]),
                Call(call_type=CallType.PAIR, tiles=[36, 36]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[26, 26, 26]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"HALF_FLUSH": 1, "ALL_GREENS": 1})

    def test_all_terminals(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[1, 1, 1]),
                Call(call_type=CallType.PON, tiles=[11, 11, 11]),
                Call(call_type=CallType.PON, tiles=[29, 29, 29]),
                Call(call_type=CallType.PAIR, tiles=[21, 21]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[19, 19, 19]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults, {"ALL_TRIPLETS": 1, "FULLY_OUTSIDE_HAND": 1, "ALL_TERMINALS": 1}
        )

    def test_thirteen_orphans(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(
                    call_type=CallType.THIRTEEN_ORPHANS,
                    tiles=[1, 9, 11, 19, 21, 29, 31, 32, 32, 33, 34, 35, 36, 37],
                )
            ],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"THIRTEEN_ORPHANS": 1})

    def test_four_quads(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[33, 33]),
            ],
            calls=[
                Call(call_type=CallType.OPEN_KAN, tiles=[1, 1, 1, 1]),
                Call(call_type=CallType.ADD_KAN, tiles=[15, 15, 15, 15]),
                Call(call_type=CallType.ADD_KAN, tiles=[23, 23, 23, 23]),
                Call(call_type=CallType.CLOSED_KAN, tiles=[19, 19, 19, 19]),
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"ALL_TRIPLETS": 1, "FOUR_QUADS": 1})

    def test_nine_gates(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[1, 1, 1]),
                Call(call_type=CallType.CHI, tiles=[2, 3, 4]),
                Call(call_type=CallType.CHI, tiles=[4, 5, 6]),
                Call(call_type=CallType.CHI, tiles=[7, 8, 9]),
                Call(call_type=CallType.PAIR, tiles=[9, 9]),
            ],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1, "NINE_GATES": 1}
        )

    def test_full_flush_not_nine_gates(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[1, 2, 3]),
                Call(call_type=CallType.CHI, tiles=[5, 6, 7]),
                Call(call_type=CallType.PON, tiles=[9, 9, 9]),
                Call(call_type=CallType.PAIR, tiles=[3, 3]),
                Call(call_type=CallType.CHI, tiles=[3, 4, 5]),
            ],
            calls=[
                Call(call_type=CallType.FLOWER, tiles=[42]),
            ],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1})
