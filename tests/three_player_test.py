import unittest

from zundamahjong.mahjong.game import Game
from zundamahjong.mahjong.game_options import GameOptions


class ThreePlayerTest(unittest.TestCase):
    def test_3_player_game(self) -> None:
        game = Game(options=GameOptions(player_count=3))
        self.assertEqual(game.player_count, 3)
