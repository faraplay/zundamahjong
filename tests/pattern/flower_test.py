from unittest import TestCase

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType

from .get_pattern_mults import get_pattern_mults


class FlowerTest(TestCase):
    def test_no_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NO_FLOWERS": 1,
            },
        )

    def test_seat_flower(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
            },
        )

    def test_sub_round_seat_flower(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[440],
            sub_round=1,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
            },
        )

    def test_two_seat_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410, 450],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 2,
            },
        )

    def test_set_of_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410, 420, 430, 440],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
                "SET_OF_FLOWERS": 1,
            },
        )

    def test_three_player_set_of_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=2,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410, 420, 430],
            player_count=3,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "SEAT_FLOWER": 1,
                "SET_OF_FLOWERS": 1,
            },
        )

    def test_three_player_five_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=2,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410, 420, 430, 460, 470],
            player_count=3,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "SEAT_FLOWER": 1,
                "SET_OF_FLOWERS": 1,
                "FIVE_FLOWERS": 1,
            },
        )

    def test_seven_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410, 420, 430, 440, 460, 470, 480],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 1,
                "SET_OF_FLOWERS": 1,
                "SEVEN_FLOWERS": 1,
            },
        )

    def test_two_sets_of_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=3,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410, 420, 430, 440, 450, 460, 470, 480],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "NON_PINFU_TSUMO": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "SEAT_FLOWER": 2,
                "TWO_SETS_OF_FLOWERS": 1,
            },
        )

    def test_three_player_two_sets_of_flowers(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=2,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[410, 420, 430, 450, 460, 470],
            player_count=3,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "SEAT_FLOWER": 2,
                "TWO_SETS_OF_FLOWERS": 1,
            },
        )
