from unittest import TestCase

from src.mahjong.call import (
    AddKanCall,
    CallType,
    ClosedKanCall,
    OpenCall,
    OpenKanCall,
)
from src.mahjong.meld import Meld, MeldType
from tests.yaku_test import get_yaku_mults


class YakumanTest(TestCase):
    def test_blessing_of_heaven(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[],
            flowers=[420],
            is_tenhou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_HEAVEN": 1})

    def test_blessing_of_earth(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.CHI, tiles=[230, 240, 250]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[],
            flowers=[430],
            is_chiihou=True,
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "BLESSING_OF_EARTH": 1})

    def test_little_three_dragons(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.PON, tiles=[350, 351, 352]),
                Meld(meld_type=MeldType.PON, tiles=[230, 231, 232]),
                Meld(meld_type=MeldType.PAIR, tiles=[360, 361]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=370,
                    other_tiles=(371, 372),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults, {"WHITE_DRAGON": 1, "RED_DRAGON": 1, "LITTLE_THREE_DRAGONS": 1}
        )

    def test_big_three_dragons(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.PON, tiles=[350, 351, 352]),
                Meld(meld_type=MeldType.PON, tiles=[360, 361, 362]),
                Meld(meld_type=MeldType.PAIR, tiles=[230, 231]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=370,
                    other_tiles=(371, 372),
                ),
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

    def test_four_little_winds(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[20, 30, 40]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
                Meld(meld_type=MeldType.PAIR, tiles=[310, 311]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=320,
                    other_tiles=(321, 322),
                ),
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

    def test_four_big_winds(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[310, 311, 312]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
                Meld(meld_type=MeldType.PAIR, tiles=[30, 31]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=320,
                    other_tiles=(321, 322),
                ),
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

    def test_four_concealed_triplets(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[230, 231, 232]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                ClosedKanCall(
                    call_type=CallType.CLOSED_KAN, tiles=(190, 191, 192, 193)
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "ALL_TRIPLETS": 1, "FOUR_CONCEALED_TRIPLETS": 1}
        )

    def test_all_honours(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[360, 361, 362]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
                Meld(meld_type=MeldType.PAIR, tiles=[350, 351]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=320,
                    other_tiles=(321, 322),
                ),
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

    def test_all_greens(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[220, 230, 240]),
                Meld(meld_type=MeldType.PON, tiles=[231, 232, 233]),
                Meld(meld_type=MeldType.CHI, tiles=[280, 281, 282]),
                Meld(meld_type=MeldType.PAIR, tiles=[360, 361]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=260,
                    other_tiles=(261, 262),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"HALF_FLUSH": 1, "ALL_GREENS": 1})

    def test_all_terminals(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.PON, tiles=[110, 111, 112]),
                Meld(meld_type=MeldType.PON, tiles=[290, 291, 292]),
                Meld(meld_type=MeldType.PAIR, tiles=[210, 211]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=190,
                    other_tiles=(191, 192),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults, {"ALL_TRIPLETS": 1, "FULLY_OUTSIDE_HAND": 1, "ALL_TERMINALS": 1}
        )

    def test_thirteen_orphans(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.THIRTEEN_ORPHANS,
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

    def test_four_quads(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenKanCall(
                    called_player_index=0, called_tile=10, other_tiles=(11, 12, 13)
                ),
                AddKanCall(
                    called_player_index=0,
                    called_tile=150,
                    added_tile=151,
                    other_tiles=(152, 153),
                ),
                AddKanCall(
                    called_player_index=0,
                    called_tile=230,
                    added_tile=231,
                    other_tiles=(232, 233),
                ),
                ClosedKanCall(tiles=(190, 191, 192, 193)),
            ],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"ALL_TRIPLETS": 1, "FOUR_QUADS": 1})

    def test_nine_gates(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.CHI, tiles=[20, 30, 40]),
                Meld(meld_type=MeldType.CHI, tiles=[41, 50, 60]),
                Meld(meld_type=MeldType.CHI, tiles=[70, 80, 90]),
                Meld(meld_type=MeldType.PAIR, tiles=[91, 92]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(
            yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1, "NINE_GATES": 1}
        )

    def test_full_flush_not_nine_gates(self) -> None:
        yaku_mults = get_yaku_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30]),
                Meld(meld_type=MeldType.CHI, tiles=[50, 60, 70]),
                Meld(meld_type=MeldType.PON, tiles=[90, 91, 92]),
                Meld(meld_type=MeldType.PAIR, tiles=[31, 32]),
                Meld(meld_type=MeldType.CHI, tiles=[33, 40, 51]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(yaku_mults, {"NO_CALLS": 1, "FULL_FLUSH": 1})
