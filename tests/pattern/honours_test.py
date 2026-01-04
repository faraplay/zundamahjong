from unittest import TestCase

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType

from .get_pattern_mults import get_pattern_mults


class HonoursTest(TestCase):
    def test_little_three_dragons(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
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
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "SIMPLE_CLOSED_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "YAKUHAI_PAIR": 1,
                "NON_PINFU_TSUMO": 1,
                "WHITE_DRAGON": 1,
                "RED_DRAGON": 1,
                "LITTLE_THREE_DRAGONS": 1,
            },
        )

    def test_big_three_dragons(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
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
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "NON_PINFU_TSUMO": 1,
                "WHITE_DRAGON": 1,
                "GREEN_DRAGON": 1,
                "RED_DRAGON": 1,
                "BIG_THREE_DRAGONS": 1,
            },
        )

    def test_four_little_winds(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[20, 30, 40], winning_tile_index=0),
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
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "YAKUHAI_PAIR": 2,
                "NON_PINFU_TSUMO": 1,
                "HALF_FLUSH": 1,
                "FOUR_LITTLE_WINDS": 1,
            },
        )

    def test_four_big_winds(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(
                    meld_type=MeldType.PON, tiles=[310, 311, 312], winning_tile_index=0
                ),
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
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 2,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "SEAT_WIND": 1,
                "PREVALENT_WIND": 1,
                "HALF_FLUSH": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_BIG_WINDS": 1,
            },
        )

    def test_all_honours(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(
                    meld_type=MeldType.PON, tiles=[360, 361, 362], winning_tile_index=0
                ),
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
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 2,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "YAKUHAI_PAIR": 1,
                "GREEN_DRAGON": 1,
                "ALL_TRIPLETS": 1,
                "ALL_HONOURS": 1,
            },
        )
