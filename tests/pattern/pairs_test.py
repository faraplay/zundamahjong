from unittest import TestCase
from .get_pattern_mults import get_pattern_mults

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType


class PairsTest(TestCase):
    def test_seven_pairs(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=1,
            formed_hand=[
                Meld(meld_type=MeldType.PAIR, tiles=[30, 31], winning_tile_index=0),
                Meld(meld_type=MeldType.PAIR, tiles=[40, 41]),
                Meld(meld_type=MeldType.PAIR, tiles=[90, 91]),
                Meld(meld_type=MeldType.PAIR, tiles=[150, 151]),
                Meld(meld_type=MeldType.PAIR, tiles=[210, 211]),
                Meld(meld_type=MeldType.PAIR, tiles=[220, 221]),
                Meld(meld_type=MeldType.PAIR, tiles=[310, 311]),
            ],
            calls=[],
            flowers=[420],
        )
        self.assertDictEqual(pattern_mults, {"SEVEN_PAIRS": 1})

    def test_eyes(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.PON, tiles=[190, 191, 192], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.PAIR, tiles=[80, 81]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=10,
                    other_tiles=(20, 30),
                ),
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=150,
                    other_tiles=(160, 170),
                ),
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
                "DUAL_PON_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "EYES": 1,
            },
        )
