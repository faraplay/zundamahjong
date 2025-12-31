from unittest import TestCase
from .get_pattern_mults import get_pattern_mults


from zundamahjong.mahjong.call import (
    AddKanCall,
    CallType,
    ClosedKanCall,
    OpenCall,
    OpenKanCall,
)
from zundamahjong.mahjong.meld import Meld, MeldType


class SetsTest(TestCase):
    def test_all_triplets(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(231, 232),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "SIMPLE_OPEN_TRIPLET": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "SIMPLE_CLOSED_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "ALL_TRIPLETS": 1,
            },
        )

    def test_triple_triplets(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[90, 91, 92], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.PON,
                    called_player_index=3,
                    called_tile=290,
                    other_tiles=(291, 292),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "NON_PINFU_TSUMO": 1,
                "TRIPLE_TRIPLETS": 1,
            },
        )

    def test_three_concealed_triplets(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331], winning_tile_index=0),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "PAIR_WAIT": 1,
                "SIMPLE_CLOSED_TRIPLET": 1,
                "ORPHAN_CLOSED_TRIPLET": 2,
                "THREE_CONCEALED_TRIPLETS": 1,
            },
        )

    def test_four_concealed_triplets(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
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
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "SIMPLE_CLOSED_TRIPLET": 2,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "ORPHAN_CLOSED_QUAD": 1,
                "NON_PINFU_TSUMO": 1,
                "NO_CALLS": 1,
                "NO_CALLS_TSUMO": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_CONCEALED_TRIPLETS": 1,
            },
        )

    def test_one_open_triplet(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12], winning_tile_index=0),
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
            pattern_mults,
            {
                "DUAL_PON_WAIT": 1,
                "ORPHAN_OPEN_TRIPLET": 1,
                "SIMPLE_CLOSED_TRIPLET": 2,
                "ORPHAN_CLOSED_QUAD": 1,
                "NO_CALLS_RON": 1,
                "NO_CALLS": 1,
                "ALL_TRIPLETS": 1,
                "THREE_CONCEALED_TRIPLETS": 1,
            },
        )

    def test_four_concealed_triplets_1_sided_wait(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PON, tiles=[10, 11, 12]),
                Meld(meld_type=MeldType.PON, tiles=[150, 151, 152]),
                Meld(meld_type=MeldType.PON, tiles=[230, 231, 232]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331], winning_tile_index=0),
            ],
            calls=[
                ClosedKanCall(
                    call_type=CallType.CLOSED_KAN, tiles=(190, 191, 192, 193)
                ),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "PAIR_WAIT": 1,
                "SIMPLE_CLOSED_TRIPLET": 2,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "ORPHAN_CLOSED_QUAD": 1,
                "NO_CALLS_RON": 1,
                "NO_CALLS": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT": 1,
            },
        )

    def test_three_quads(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[110, 120, 130], winning_tile_index=0
                ),
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
                ClosedKanCall(tiles=(190, 191, 192, 193)),
            ],
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "SIMPLE_OPEN_QUAD": 1,
                "ORPHAN_OPEN_QUAD": 1,
                "ORPHAN_CLOSED_QUAD": 1,
                "NON_PINFU_TSUMO": 1,
                "THREE_QUADS": 1,
            },
        )

    def test_four_quads(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331], winning_tile_index=0),
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
        self.assertDictEqual(
            pattern_mults,
            {
                "PAIR_WAIT": 1,
                "SIMPLE_OPEN_QUAD": 2,
                "ORPHAN_OPEN_QUAD": 1,
                "ORPHAN_CLOSED_QUAD": 1,
                "NON_PINFU_TSUMO": 1,
                "ALL_TRIPLETS": 1,
                "FOUR_QUADS": 1,
            },
        )
