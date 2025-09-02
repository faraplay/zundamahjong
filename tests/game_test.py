import unittest

from src.mahjong.action import Action, ActionType
from src.mahjong.round import RoundStatus
from src.mahjong.game import Game

from decks import *


class GameTest(unittest.TestCase):
    def test_first_game(self):
        game = Game(test_deck2)
        self.assertEqual(game.wind_round, 0)
        self.assertEqual(game.sub_round, 0)
        self.assertSequenceEqual(game.player_scores, [0, 0, 0, 0])

    def test_no_winscoring_during_first_game(self):
        game = Game(test_deck2)
        self.assertIsNone(game.win_scoring)

    def test_auto_calculate_score(self):
        game = Game(test_deck2)
        game.round.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        game.round.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(game.round.status, RoundStatus.END)
        self.assertIsNotNone(game.win_scoring)
        self.assertSequenceEqual(
            game.player_scores, game.win_scoring.scoring.seat_scores
        )
