import unittest

from src.mahjong.game_options import GameOptions
from src.mahjong.game import Game

from tests.decks import *


class ThreePlayerTest(unittest.TestCase):
    def test_3_player_game(self):
        game = Game(options=GameOptions(player_count=3))
        self.assertEqual(game._player_count, 3)
