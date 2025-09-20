import unittest

from src.mahjong.exceptions import InvalidOperationException
from src.mahjong.action import Action, ActionType
from src.mahjong.game_options import GameOptions
from src.mahjong.round import RoundStatus
from src.mahjong.game import Game

from decks import *


class GameTest(unittest.TestCase):
    def test_first_round(self):
        game = Game(first_deck_tiles=test_deck2)
        self.assertEqual(game.wind_round, 0)
        self.assertEqual(game.sub_round, 0)
        self.assertSequenceEqual(game.player_scores, [0, 0, 0, 0])

    def test_no_win_during_first_round(self):
        game = Game(first_deck_tiles=test_deck2)
        self.assertIsNone(game.win)

    def test_cannot_start_next_round_during_round(self):
        game = Game(first_deck_tiles=test_deck2)
        with self.assertRaises(InvalidOperationException):
            game.start_next_round(test_deck2)

    def test_auto_calculate_score(self):
        game = Game(first_deck_tiles=test_deck2)
        game.round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(2, Action(action_type=ActionType.RON))
        self.assertIsNotNone(game.win)
        self.assertSequenceEqual(game.player_scores, game.scoring.player_scores)

    def test_dealer_repeat_next_round(self):
        game = Game(first_deck_tiles=test_deck6)
        game.round.do_action(0, Action(action_type=ActionType.TSUMO))
        game.start_next_round(test_deck2)
        self.assertEqual(game.wind_round, 0)
        self.assertEqual(game.sub_round, 0)

    def test_dealer_nonrepeat_next_round(self):
        game = Game(first_deck_tiles=test_deck2)
        game.round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(2, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        self.assertEqual(game.wind_round, 0)
        self.assertEqual(game.sub_round, 1)

    def test_next_wind_round(self):
        game = Game(
            first_deck_tiles=test_deck2, options=GameOptions(game_length=(2, 0))
        )
        game.round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(2, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(1, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(3, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(2, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(0, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(3, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(1, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        self.assertEqual(game.wind_round, 1)
        self.assertEqual(game.sub_round, 0)
        self.assertEqual(game.round._wind_round, 1)

    def test_one_round_game(self):
        game = Game(
            first_deck_tiles=test_deck2, options=GameOptions(game_length=(0, 1))
        )
        game.round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(2, Action(action_type=ActionType.RON))
        self.assertTrue(game.is_game_end)

    def test_cannot_start_next_round_at_end(self):
        game = Game(
            first_deck_tiles=test_deck2, options=GameOptions(game_length=(0, 1))
        )
        game.round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(2, Action(action_type=ActionType.RON))
        with self.assertRaises(InvalidOperationException):
            game.start_next_round()

    def test_last_round_dealer_repeat(self):
        game = Game(
            first_deck_tiles=test_deck2, options=GameOptions(game_length=(1, 0))
        )
        game.round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(2, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(1, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(3, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(2, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(0, Action(action_type=ActionType.RON))
        game.start_next_round(test_deck6)
        game.round.do_action(3, Action(action_type=ActionType.TSUMO))
        self.assertFalse(game.is_game_end)
        game.start_next_round(test_deck2)
        game.round.do_action(3, Action(action_type=ActionType.DISCARD, tile=52))
        game.round.do_action(1, Action(action_type=ActionType.RON))
        self.assertTrue(game.is_game_end)

    def test_draw_count(self):
        game = Game(first_deck_tiles=test_deck4)
        self.assertEqual(game.draw_count, 0)
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(game.draw_count, 0)

        game.start_next_round(test_deck4)
        self.assertEqual(game.draw_count, 1)
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(game.draw_count, 1)

        game.start_next_round(test_deck6)
        self.assertEqual(game.draw_count, 2)
        game.round.do_action(0, Action(action_type=ActionType.TSUMO))
        self.assertEqual(game.draw_count, 2)

        game.start_next_round(test_deck2)
        self.assertEqual(game.draw_count, 0)

    def test_win_draw_count(self):
        game = Game(first_deck_tiles=test_deck4)
        self.assertEqual(game.draw_count, 0)
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(game.draw_count, 0)

        game.start_next_round(test_deck4)
        self.assertEqual(game.draw_count, 1)
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(game.draw_count, 1)

        game.start_next_round(test_deck6)
        self.assertEqual(game.draw_count, 2)
        game.round.do_action(0, Action(action_type=ActionType.TSUMO))
        self.assertEqual(game.win.draw_count, 2)
