import unittest

from src.mahjong.call import Call, CallType
from src.mahjong.game_options import GameOptions
from src.mahjong.game import Game
from src.mahjong.win import Win
from src.mahjong.yaku import YakuCalculator

from tests.decks import *


class ThreePlayerTest(unittest.TestCase):
    def test_3_player_game(self):
        game = Game(options=GameOptions(player_count=3))
        self.assertEqual(game._player_count, 3)

    def test_north_yaku(self):
        formed_hand = [
            Call(call_type=CallType.CHI, tiles=[84, 88, 92]),
            Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
            Call(call_type=CallType.PON, tiles=[136, 137, 138]),
            Call(call_type=CallType.PAIR, tiles=[132, 133]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[172],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        yaku_mults = YakuCalculator(win, formed_hand).get_yaku_mults()
        self.assertDictEqual(
            yaku_mults,
            {"NORTH_WIND": 1},
        )

    def test_one_set_of_flowers(self):
        formed_hand = [
            Call(call_type=CallType.CHI, tiles=[84, 88, 92]),
            Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
            Call(call_type=CallType.PON, tiles=[76, 77, 78]),
            Call(call_type=CallType.PAIR, tiles=[132, 133]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164, 168, 172],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        yaku_mults = YakuCalculator(win, formed_hand).get_yaku_mults()
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1})

    def test_five_flowers(self):
        formed_hand = [
            Call(call_type=CallType.CHI, tiles=[84, 88, 92]),
            Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
            Call(call_type=CallType.PON, tiles=[76, 77, 78]),
            Call(call_type=CallType.PAIR, tiles=[132, 133]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164, 168, 172, 184, 188],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        yaku_mults = YakuCalculator(win, formed_hand).get_yaku_mults()
        self.assertDictEqual(
            yaku_mults, {"SEAT_FLOWER": 1, "SET_OF_FLOWERS": 1, "FIVE_FLOWERS": 1}
        )

    def test_one_set_of_flowers(self):
        formed_hand = [
            Call(call_type=CallType.CHI, tiles=[84, 88, 92]),
            Call(call_type=CallType.CHI, tiles=[60, 64, 68]),
            Call(call_type=CallType.PON, tiles=[76, 77, 78]),
            Call(call_type=CallType.PAIR, tiles=[132, 133]),
        ]
        win = Win(
            win_player=0,
            lose_player=None,
            hand=[tile for call in formed_hand for tile in call.tiles],
            calls=[
                Call(call_type=CallType.CHI, tiles=[92, 96, 100]),
            ],
            flowers=[164, 168, 172, 180, 184, 188],
            player_count=3,
            wind_round=0,
            sub_round=0,
        )
        yaku_mults = YakuCalculator(win, formed_hand).get_yaku_mults()
        self.assertDictEqual(yaku_mults, {"SEAT_FLOWER": 2, "TWO_SETS_OF_FLOWERS": 1})
