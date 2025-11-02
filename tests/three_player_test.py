import unittest

from zundamahjong.mahjong.call import CallType, OpenCall
from zundamahjong.mahjong.game import Game
from zundamahjong.mahjong.game_options import GameOptions
from zundamahjong.mahjong.meld import Meld, MeldType
from zundamahjong.mahjong.pattern import PatternCalculator
from zundamahjong.mahjong.win import Win


class ThreePlayerTest(unittest.TestCase):
    def test_3_player_game(self) -> None:
        game = Game(options=GameOptions(player_count=3))
        self.assertEqual(game.player_count, 3)


class ThreePlayerPatternTest(unittest.TestCase):
    def test_north_pattern(self) -> None:
        formed_hand = [
            Meld(meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0),
            Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
            Meld(meld_type=MeldType.PON, tiles=[340, 341, 342]),
            Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
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
            wind_round=0,
            sub_round=0,
        )
        pattern_mults = PatternCalculator(win, formed_hand).get_pattern_mults()
        self.assertDictEqual(
            pattern_mults,
            {
                "OPEN_WAIT": 1,
                "ORPHAN_CLOSED_TRIPLET": 1,
                "NON_PINFU_TSUMO": 1,
                "NORTH_WIND": 1,
            },
        )

    def test_one_set_of_flowers(self) -> None:
        formed_hand = [
            Meld(meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0),
            Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
            Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
            Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
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
            wind_round=0,
            sub_round=0,
        )
        pattern_mults = PatternCalculator(win, formed_hand).get_pattern_mults()
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

    def test_five_flowers(self) -> None:
        formed_hand = [
            Meld(meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0),
            Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
            Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
            Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
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
            wind_round=0,
            sub_round=0,
        )
        pattern_mults = PatternCalculator(win, formed_hand).get_pattern_mults()
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

    def test_two_sets_of_flowers(self) -> None:
        formed_hand = [
            Meld(meld_type=MeldType.CHI, tiles=[210, 220, 230], winning_tile_index=0),
            Meld(meld_type=MeldType.CHI, tiles=[150, 160, 170]),
            Meld(meld_type=MeldType.PON, tiles=[190, 191, 192]),
            Meld(meld_type=MeldType.PAIR, tiles=[330, 331]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
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
            wind_round=0,
            sub_round=0,
        )
        pattern_mults = PatternCalculator(win, formed_hand).get_pattern_mults()
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
