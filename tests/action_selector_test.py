import unittest

from src.mahjong.action import (
    ActionType,
    ClosedKanAction,
    HandTileAction,
    OpenCallAction,
    SimpleAction,
)
from src.mahjong.round import Round, RoundStatus
from src.mahjong.action_selector import ActionSelector

from tests.decks import *


class ActionSelectorTest(unittest.TestCase):
    def test_submit_only_action(self) -> None:
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        history_updates = action_selector.submit_action(
            0,
            HandTileAction(action_type=ActionType.DISCARD, tile=130),
            len(round.history),
        )
        assert history_updates is not None
        self.assertSequenceEqual(
            history_updates,
            [(0, HandTileAction(action_type=ActionType.DISCARD, tile=130))],
        )
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.DISCARDED)

    def test_submit_low_to_high_action(self) -> None:
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0,
            HandTileAction(action_type=ActionType.DISCARD, tile=130),
            len(round.history),
        )
        history_updates = action_selector.submit_action(
            0, SimpleAction(action_type=ActionType.PASS), len(round.history)
        )
        assert history_updates is not None
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            1,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)),
            len(round.history),
        )
        assert history_updates is not None
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            2,
            OpenCallAction(action_type=ActionType.PON, other_tiles=(131, 132)),
            len(round.history),
        )
        assert history_updates is not None
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            3, SimpleAction(action_type=ActionType.RON), len(round.history)
        )
        assert history_updates is not None
        self.assertSequenceEqual(
            history_updates, [(3, SimpleAction(action_type=ActionType.RON))]
        )

    def test_submit_high_action(self) -> None:
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0,
            HandTileAction(action_type=ActionType.DISCARD, tile=130),
            len(round.history),
        )
        history_updates = action_selector.submit_action(
            3, SimpleAction(action_type=ActionType.RON), len(round.history)
        )
        assert history_updates is not None
        self.assertSequenceEqual(
            history_updates, [(3, SimpleAction(action_type=ActionType.RON))]
        )

    def test_do_auto_draw(self) -> None:
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        history_updates = action_selector.submit_action(
            0,
            HandTileAction(action_type=ActionType.DISCARD, tile=10),
            len(round.history),
        )
        assert history_updates is not None
        self.assertSequenceEqual(
            history_updates,
            [
                (0, HandTileAction(action_type=ActionType.DISCARD, tile=10)),
                (1, SimpleAction(action_type=ActionType.DRAW)),
            ],
        )

    def test_submit_bad_action(self) -> None:
        round = Round(tiles=test_deck4)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0,
            HandTileAction(action_type=ActionType.DISCARD, tile=130),
            len(round.history),
        )
        history_updates = action_selector.submit_action(
            3, SimpleAction(action_type=ActionType.PASS), len(round.history)
        )
        assert history_updates is not None
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            1,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)),
            len(round.history),
        )
        assert history_updates is not None
        self.assertSequenceEqual(history_updates, [])
        history_updates = action_selector.submit_action(
            2, SimpleAction(action_type=ActionType.RON), len(round.history)
        )
        assert history_updates is not None
        self.assertSequenceEqual(
            history_updates,
            [(1, OpenCallAction(action_type=ActionType.CHII, other_tiles=(110, 120)))],
        )

    def test_do_auto_continue(self) -> None:
        round = Round(tiles=test_deck_one_discard_option)
        action_selector = ActionSelector(round)
        history_updates = action_selector.submit_action(
            0,
            ClosedKanAction(tiles=(110, 111, 112, 113)),
            len(round.history),
        )
        assert history_updates is not None
        self.assertSequenceEqual(
            history_updates,
            [
                (0, ClosedKanAction(tiles=(110, 111, 112, 113))),
                (0, SimpleAction(action_type=ActionType.CONTINUE)),
            ],
        )

    def test_do_not_auto_discard(self) -> None:
        round = Round(tiles=test_deck_one_discard_option)
        action_selector = ActionSelector(round)
        action_selector.submit_action(
            0,
            ClosedKanAction(tiles=(110, 111, 112, 113)),
            len(round.history),
        )
        action_selector.submit_action(
            0,
            ClosedKanAction(tiles=(120, 121, 122, 123)),
            len(round.history),
        )
        action_selector.submit_action(
            0,
            ClosedKanAction(tiles=(130, 131, 132, 133)),
            len(round.history),
        )
        action_selector.submit_action(
            0,
            HandTileAction(action_type=ActionType.DISCARD, tile=320),
            len(round.history),
        )
        action_selector.submit_action(
            1,
            HandTileAction(action_type=ActionType.DISCARD, tile=140),
            len(round.history),
        )
        history_updates = action_selector.submit_action(
            0,
            OpenCallAction(action_type=ActionType.PON, other_tiles=(141, 142)),
            len(round.history),
        )
        assert history_updates is not None
        self.assertSequenceEqual(
            history_updates,
            [(0, OpenCallAction(action_type=ActionType.PON, other_tiles=(141, 142)))],
        )
