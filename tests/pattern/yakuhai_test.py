from unittest import TestCase
from .get_pattern_mults import get_pattern_mults

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.meld import Meld, MeldType


class YakuhaiTest(TestCase):
    def test_seat_wind(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[320, 321, 322]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=0,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "SEAT_WIND": 1,
            },
        )

    def test_sub_round_seat_wind(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=2,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[320, 321, 322]),
                Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=1,
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
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "SEAT_WIND": 1,
            },
        )

    def test_prevalent_wind(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[310, 311, 312]),
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
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "PREVALENT_WIND": 1,
            },
        )

    def test_north_wind(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(
                    meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0
                ),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
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
            flowers=[430],
            player_count=3,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "NORTH_WIND": 1,
            },
        )

    def test_white_dragon(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[350, 351, 352]),
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
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "WHITE_DRAGON": 1,
            },
        )

    def test_green_dragon(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[360, 361, 362]),
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
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "GREEN_DRAGON": 1,
            },
        )

    def test_red_dragon(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[370, 371, 372]),
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
            flowers=[420],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "RED_DRAGON": 1,
            },
        )

    def test_seat_wind_pair(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PAIR, tiles=[320, 321]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=0,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[440],
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "YAKUHAI_PAIR": 1,
            },
        )

    def test_sub_round_seat_wind_pair(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=2,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PAIR, tiles=[320, 321]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=1,
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
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "YAKUHAI_PAIR": 1,
            },
        )

    def test_prevalent_wind_pair(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=1,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PAIR, tiles=[310, 311]),
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
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "YAKUHAI_PAIR": 1,
            },
        )

    def test_north_wind_pair(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PAIR, tiles=[340, 341]),
            ],
            calls=[
                OpenCall(
                    call_type=CallType.CHI,
                    called_player_index=2,
                    called_tile=230,
                    other_tiles=(240, 250),
                ),
            ],
            flowers=[430],
            player_count=3,
        )
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "YAKUHAI_PAIR": 1,
            },
        )

    def test_white_dragon_pair(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PAIR, tiles=[350, 351]),
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
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "YAKUHAI_PAIR": 1,
            },
        )

    def test_green_dragon_pair(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PAIR, tiles=[360, 361]),
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
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "YAKUHAI_PAIR": 1,
            },
        )

    def test_red_dragon_pair(self) -> None:
        pattern_mults = get_pattern_mults(
            win_player=0,
            lose_player=None,
            formed_hand=[
                Meld(meld_type=MeldType.CHI, tiles=[10, 20, 30], winning_tile_index=0),
                Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
                Meld(meld_type=MeldType.PON, tiles=[330, 331, 332]),
                Meld(meld_type=MeldType.PAIR, tiles=[370, 371]),
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
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "YAKUHAI_PAIR": 1,
            },
        )
