from unittest import TestCase

from src.mahjong.call import Call, CallType
from tests.yaku_test import get_yaku_mults


class YakumanTest(TestCase):
    def test_blessing_of_heaven(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[10, 20, 30]),
                Call(call_type=CallType.CHI, tiles=[150, 160, 170]),
                Call(call_type=CallType.PON, tiles=[190, 191, 192]),
                Call(call_type=CallType.CHI, tiles=[230, 240, 250]),
                Call(call_type=CallType.PAIR, tiles=[330, 331]),
            ],
            calls=[],
            flowers=[420],
            is_tenhou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_HEAVEN": 1})

    def test_blessing_of_earth(self):
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[10, 20, 30]),
                Call(call_type=CallType.CHI, tiles=[150, 160, 170]),
                Call(call_type=CallType.PON, tiles=[190, 191, 192]),
                Call(call_type=CallType.CHI, tiles=[230, 240, 250]),
                Call(call_type=CallType.PAIR, tiles=[330, 331]),
            ],
            calls=[],
            flowers=[430],
            is_chiihou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_EARTH": 1})

    def test_little_three_dragons(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[10, 20, 30]),
                Call(call_type=CallType.PON, tiles=[350, 351, 352]),
                Call(call_type=CallType.PON, tiles=[230, 231, 232]),
                Call(call_type=CallType.PAIR, tiles=[360, 361]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[370, 371, 372]),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults, {"WHITE_DRAGON": 1, "RED_DRAGON": 1, "LITTLE_THREE_DRAGONS": 1}
        )

    def test_big_three_dragons(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[10, 20, 30]),
                Call(call_type=CallType.PON, tiles=[350, 351, 352]),
                Call(call_type=CallType.PON, tiles=[360, 361, 362]),
                Call(call_type=CallType.PAIR, tiles=[230, 231]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[370, 371, 372]),
            ],
            flowers=[420],
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
                Call(call_type=CallType.CHI, tiles=[20, 30, 40]),
                Call(call_type=CallType.PON, tiles=[330, 331, 332]),
                Call(call_type=CallType.PON, tiles=[340, 341, 342]),
                Call(call_type=CallType.PAIR, tiles=[310, 311]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[320, 321, 322]),
            ],
            flowers=[420],
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
                Call(call_type=CallType.PON, tiles=[310, 311, 312]),
                Call(call_type=CallType.PON, tiles=[330, 331, 332]),
                Call(call_type=CallType.PON, tiles=[340, 341, 342]),
                Call(call_type=CallType.PAIR, tiles=[30, 31]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[320, 321, 322]),
            ],
            flowers=[420],
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
                Call(call_type=CallType.PON, tiles=[10, 11, 12]),
                Call(call_type=CallType.PON, tiles=[150, 151, 152]),
                Call(call_type=CallType.PON, tiles=[230, 231, 232]),
                Call(call_type=CallType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                Call(call_type=CallType.CLOSED_KAN, tiles=[190, 191, 192, 193]),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "ALL_TRIPLETS": 1, "FOUR_CONCEALED_TRIPLETS": 1}
        )

    def test_all_honours(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[360, 361, 362]),
                Call(call_type=CallType.PON, tiles=[330, 331, 332]),
                Call(call_type=CallType.PON, tiles=[340, 341, 342]),
                Call(call_type=CallType.PAIR, tiles=[350, 351]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[320, 321, 322]),
            ],
            flowers=[420],
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
                Call(call_type=CallType.CHI, tiles=[220, 230, 240]),
                Call(call_type=CallType.PON, tiles=[231, 232, 233]),
                Call(call_type=CallType.CHI, tiles=[280, 281, 282]),
                Call(call_type=CallType.PAIR, tiles=[360, 361]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[260, 261, 262]),
            ],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"HALF_FLUSH": 1, "ALL_GREENS": 1})

    def test_all_terminals(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[10, 11, 12]),
                Call(call_type=CallType.PON, tiles=[110, 111, 112]),
                Call(call_type=CallType.PON, tiles=[290, 291, 292]),
                Call(call_type=CallType.PAIR, tiles=[210, 211]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[190, 191, 192]),
            ],
            flowers=[420],
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
                    tiles=[
                        4,
                        36,
                        44,
                        76,
                        84,
                        116,
                        124,
                        128,
                        129,
                        132,
                        136,
                        140,
                        144,
                        148,
                    ],
                ),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"THIRTEEN_ORPHANS": 1})

    def test_four_quads(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                Call(call_type=CallType.OPEN_KAN, tiles=[10, 11, 12, 13]),
                Call(call_type=CallType.ADD_KAN, tiles=[150, 151, 152, 153]),
                Call(call_type=CallType.ADD_KAN, tiles=[230, 231, 232, 233]),
                Call(call_type=CallType.CLOSED_KAN, tiles=[190, 191, 192, 193]),
            ],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"ALL_TRIPLETS": 1, "FOUR_QUADS": 1})

    def test_nine_gates(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[10, 11, 12]),
                Call(call_type=CallType.CHI, tiles=[20, 30, 40]),
                Call(call_type=CallType.CHI, tiles=[41, 50, 60]),
                Call(call_type=CallType.CHI, tiles=[70, 80, 90]),
                Call(call_type=CallType.PAIR, tiles=[91, 92]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1, "NINE_GATES": 1}
        )

    def test_full_flush_not_nine_gates(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[10, 20, 30]),
                Call(call_type=CallType.CHI, tiles=[50, 60, 70]),
                Call(call_type=CallType.PON, tiles=[90, 91, 92]),
                Call(call_type=CallType.PAIR, tiles=[31, 32]),
                Call(call_type=CallType.CHI, tiles=[33, 40, 51]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1})
