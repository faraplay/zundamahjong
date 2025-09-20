from unittest import TestCase

from src.mahjong.call import Call, CallType
from tests.yaku_test import get_yaku_mults


class YakumanTest(TestCase):
    def test_blessing_of_heaven(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[],
            flowers=[168],
            is_tenhou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_HEAVEN": 1})

    def test_blessing_of_earth(self):
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[],
            flowers=[172],
            is_chiihou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_EARTH": 1})

    def test_little_three_dragons(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.PON, tiles=[140, 141, 142]),
                Call(call_type=CallType.PON, tiles=[92, 93, 94]),
                Call(call_type=CallType.PAIR, tiles=[144, 145]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[148, 149, 150]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(
            yaku_mults, {"WHITE_DRAGON": 1, "RED_DRAGON": 1, "LITTLE_THREE_DRAGONS": 1}
        )

    def test_big_three_dragons(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.PON, tiles=[140, 141, 142]),
                Call(call_type=CallType.PON, tiles=[144, 145, 146]),
                Call(call_type=CallType.PAIR, tiles=[92, 93]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[148, 149, 150]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[8, 12, 16]),
                Call(call_type=CallType.PON, tiles=[132, 133, 134]),
                Call(call_type=CallType.PON, tiles=[136, 137, 138]),
                Call(call_type=CallType.PAIR, tiles=[124, 125]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[128, 129, 130]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.PON, tiles=[124, 125, 126]),
                Call(call_type=CallType.PON, tiles=[132, 133, 134]),
                Call(call_type=CallType.PON, tiles=[136, 137, 138]),
                Call(call_type=CallType.PAIR, tiles=[12, 13]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[128, 129, 130]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.PON, tiles=[4, 5, 6]),
                Call(call_type=CallType.PON, tiles=[60, 61, 62]),
                Call(call_type=CallType.PON, tiles=[92, 93, 94]),
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.CLOSED_KAN, tiles=[76, 77, 78, 79]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "ALL_TRIPLETS": 1, "FOUR_CONCEALED_TRIPLETS": 1}
        )

    def test_all_honours(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[144, 145, 146]),
                Call(call_type=CallType.PON, tiles=[132, 133, 134]),
                Call(call_type=CallType.PON, tiles=[136, 137, 138]),
                Call(call_type=CallType.PAIR, tiles=[140, 141]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[128, 129, 130]),
            ],
            flowers=[168],
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
                Call(call_type=CallType.CHI, tiles=[88, 92, 96]),
                Call(call_type=CallType.PON, tiles=[93, 94, 95]),
                Call(call_type=CallType.CHI, tiles=[112, 113, 114]),
                Call(call_type=CallType.PAIR, tiles=[144, 145]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[104, 105, 106]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"HALF_FLUSH": 1, "ALL_GREENS": 1})

    def test_all_terminals(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[4, 5, 6]),
                Call(call_type=CallType.PON, tiles=[44, 45, 46]),
                Call(call_type=CallType.PON, tiles=[116, 117, 118]),
                Call(call_type=CallType.PAIR, tiles=[84, 85]),
            ],
            calls=[
                Call(call_type=CallType.PON, tiles=[76, 77, 78]),
            ],
            flowers=[168],
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
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"THIRTEEN_ORPHANS": 1})

    def test_four_quads(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PAIR, tiles=[132, 133]),
            ],
            calls=[
                Call(call_type=CallType.OPEN_KAN, tiles=[4, 5, 6, 7]),
                Call(call_type=CallType.ADD_KAN, tiles=[60, 61, 62, 63]),
                Call(call_type=CallType.ADD_KAN, tiles=[92, 93, 94, 95]),
                Call(call_type=CallType.CLOSED_KAN, tiles=[76, 77, 78, 79]),
            ],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"ALL_TRIPLETS": 1, "FOUR_QUADS": 1})

    def test_nine_gates(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.PON, tiles=[4, 5, 6]),
                Call(call_type=CallType.CHI, tiles=[8, 12, 16]),
                Call(call_type=CallType.CHI, tiles=[17, 20, 24]),
                Call(call_type=CallType.CHI, tiles=[28, 32, 36]),
                Call(call_type=CallType.PAIR, tiles=[37, 38]),
            ],
            calls=[],
            flowers=[168],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1, "NINE_GATES": 1}
        )

    def test_full_flush_not_nine_gates(self):
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Call(call_type=CallType.CHI, tiles=[4, 8, 12]),
                Call(call_type=CallType.CHI, tiles=[20, 24, 28]),
                Call(call_type=CallType.PON, tiles=[36, 37, 38]),
                Call(call_type=CallType.PAIR, tiles=[13, 14]),
                Call(call_type=CallType.CHI, tiles=[15, 16, 21]),
            ],
            calls=[],
            flowers=[168],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1})
