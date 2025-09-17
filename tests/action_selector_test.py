import unittest

from src.mahjong.action import Action, ActionType
from src.mahjong.round import Round, RoundStatus
from src.mahjong.action_selector import ActionSelector

from tests.decks import *


class ActionSelectorTest(unittest.TestCase):
    def test_submit_only_action(self):
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        history_updates = action_selector.submit_action(
            0, Action(action_type=ActionType.DISCARD, tile=13)
        )
        self.assertSequenceEqual(
            history_updates, [(0, Action(action_type=ActionType.DISCARD, tile=13))]
        )
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.DISCARDED)

    def test_submit_low_to_high_action(self):
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0, Action(action_type=ActionType.DISCARD, tile=13)
        )
        history_updates = action_selector.submit_action(
            0, Action(action_type=ActionType.PASS)
        )
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            1, Action(action_type=ActionType.CHI_C)
        )
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            2, Action(action_type=ActionType.PON)
        )
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            3, Action(action_type=ActionType.RON)
        )
        self.assertSequenceEqual(
            history_updates, [(3, Action(action_type=ActionType.RON))]
        )

    def test_submit_high_action(self):
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0, Action(action_type=ActionType.DISCARD, tile=13)
        )
        history_updates = action_selector.submit_action(
            3, Action(action_type=ActionType.RON)
        )
        self.assertSequenceEqual(
            history_updates, [(3, Action(action_type=ActionType.RON))]
        )

    def test_do_auto_draw(self):
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        history_updates = action_selector.submit_action(
            0, Action(action_type=ActionType.DISCARD, tile=1)
        )
        self.assertSequenceEqual(
            history_updates,
            [
                (0, Action(action_type=ActionType.DISCARD, tile=1)),
                (1, Action(action_type=ActionType.DRAW)),
            ],
        )

    def test_submit_bad_action(self):
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0, Action(action_type=ActionType.DISCARD, tile=13)
        )
        history_updates = action_selector.submit_action(
            3, Action(action_type=ActionType.PASS)
        )
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            1, Action(action_type=ActionType.CHI_C)
        )
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            2, Action(action_type=ActionType.RON)
        )
        self.assertSequenceEqual(
            history_updates, [(1, Action(action_type=ActionType.CHI_C))]
        )

    def test_do_auto_continue(self):
        round = Round(tiles=test_deck_one_discard_option)
        action_selector = ActionSelector(round)
        history_updates = action_selector.submit_action(
            0, Action(action_type=ActionType.CLOSED_KAN, tile=11)
        )
        self.assertSequenceEqual(
            history_updates,
            [
                (0, Action(action_type=ActionType.CLOSED_KAN, tile=11)),
                (0, Action(action_type=ActionType.CONTINUE)),
            ],
        )

    def test_do_not_auto_discard(self):
        round = Round(tiles=test_deck_one_discard_option)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0, Action(action_type=ActionType.CLOSED_KAN, tile=11)
        )
        action_selector.submit_action(
            0, Action(action_type=ActionType.CLOSED_KAN, tile=12)
        )
        action_selector.submit_action(
            0, Action(action_type=ActionType.CLOSED_KAN, tile=13)
        )
        action_selector.submit_action(
            0, Action(action_type=ActionType.DISCARD, tile=32)
        )
        action_selector.submit_action(
            1, Action(action_type=ActionType.DISCARD, tile=14)
        )
        history_updates = action_selector.submit_action(
            0, Action(action_type=ActionType.PON)
        )
        self.assertSequenceEqual(
            history_updates, [(0, Action(action_type=ActionType.PON))]
        )
