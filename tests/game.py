import unittest

from src.mahjong.game import Game, GameStatus
from src.mahjong.action import Action, ActionType
from src.mahjong.call import Call, CallType

from tests.test_deck import test_deck, test_deck2


class GameTest(unittest.TestCase):
    def test_start_no_discards(self):
        game = Game()
        self.assertSequenceEqual(game.discard_pool, [])

    def test_fixed_deck(self):
        game = Game(test_deck)
        self.assertTrue(True)

    def test_fixed_deck_start_hands(self):
        game = Game(test_deck)
        self.assertSequenceEqual(
            game.get_hand(0), [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21, 21, 21]
        )
        self.assertSequenceEqual(
            game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21]
        )
        self.assertSequenceEqual(
            game.get_hand(2), [11, 11, 11, 11, 13, 13, 13, 13, 15, 15, 15, 15, 17]
        )
        self.assertSequenceEqual(
            game.get_hand(3), [12, 12, 12, 12, 14, 14, 14, 14, 16, 16, 16, 16, 17]
        )

    def test_discard_pool(self):
        game = Game(test_deck)
        game.discard(0, 17)
        self.assertSequenceEqual(game.discard_pool, [17])

    def test_discard_hand(self):
        game = Game(test_deck)
        game.discard(0, 17)
        self.assertSequenceEqual(
            game.get_hand(0), [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 21, 21]
        )

    def test_draw(self):
        game = Game(test_deck)
        game.discard(0, 17)
        game.draw(1)
        self.assertSequenceEqual(
            game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21, 1]
        )

    def test_chi_a(self):
        game = Game(test_deck)
        game.discard(0, 5)
        game.chi_a(1)
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 4, 5, 8, 9, 9, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.CHI, [5, 6, 7])])
        self.assertSequenceEqual(game.discard_pool, [])

    def test_chi_b(self):
        game = Game(test_deck)
        game.discard(0, 5)
        game.chi_b(1)
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 5, 7, 8, 9, 9, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.CHI, [4, 5, 6])])
        self.assertSequenceEqual(game.discard_pool, [])

    def test_chi_c(self):
        game = Game(test_deck)
        game.discard(0, 5)
        game.chi_c(1)
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 5, 6, 7, 8, 9, 9, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.CHI, [3, 4, 5])])
        self.assertSequenceEqual(game.discard_pool, [])

    def test_pon(self):
        game = Game(test_deck)
        game.discard(0, 9)
        game.pon(1)
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.PON, [9, 9, 9])])
        self.assertSequenceEqual(game.discard_pool, [])

    def test_pon_change_turn(self):
        game = Game(test_deck)
        game.discard(0, 1)
        game.draw(1)
        game.discard(1, 21)
        game.pon(0)
        self.assertSequenceEqual(game.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(0), [Call(CallType.PON, [21, 21, 21])])
        self.assertSequenceEqual(game.discard_pool, [1])

    def test_open_kan(self):
        game = Game(test_deck)
        game.discard(0, 9)
        game.open_kan(1)
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 17, 21, 8])
        self.assertSequenceEqual(
            game.get_calls(1), [Call(CallType.OPEN_KAN, [9, 9, 9, 9])]
        )
        self.assertSequenceEqual(game.discard_pool, [])

    def test_open_kan_change_turn(self):
        game = Game(test_deck)
        game.discard(0, 1)
        game.draw(1)
        game.discard(1, 21)
        game.open_kan(0)
        self.assertSequenceEqual(game.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 8])
        self.assertSequenceEqual(
            game.get_calls(0), [Call(CallType.OPEN_KAN, [21, 21, 21, 21])]
        )
        self.assertSequenceEqual(game.discard_pool, [1])

    def test_add_kan(self):
        game = Game(test_deck)
        game.discard(0, 9)
        game.pon(1)
        game.discard(1, 21)
        game.pon(0)
        game.discard(0, 1)
        game.draw(1)
        game.add_kan(1, 9)
        self.assertSequenceEqual(game.get_hand(1), [1, 1, 2, 3, 4, 5, 6, 7, 8, 17, 8])
        self.assertSequenceEqual(
            game.get_calls(1), [Call(CallType.ADD_KAN, [9, 9, 9, 9])]
        )
        self.assertSequenceEqual(game.discard_pool, [1])

    def test_closed_kan(self):
        game = Game(test_deck)
        game.discard(0, 1)
        game.draw(1)
        game.discard(1, 2)
        game.draw(2)
        game.closed_kan(2, 11)
        self.assertSequenceEqual(
            game.get_hand(2), [2, 13, 13, 13, 13, 15, 15, 15, 15, 17, 8]
        )
        self.assertSequenceEqual(
            game.get_calls(2), [Call(CallType.CLOSED_KAN, [11, 11, 11, 11])]
        )
        self.assertSequenceEqual(game.discard_pool, [1, 2])

    def test_discard_sort(self):
        game = Game(test_deck)
        game.discard(0, 17)
        game.draw(1)
        game.discard(1, 3)
        self.assertSequenceEqual(
            game.get_hand(1), [1, 1, 2, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21]
        )

    def test_deck_2_start_hands(self):
        game = Game(test_deck2)
        self.assertSequenceEqual(
            game.get_hand(0), [1, 1, 1, 1, 4, 4, 4, 4, 7, 7, 7, 9, 13, 36]
        )
        self.assertSequenceEqual(
            game.get_calls(0),
            [Call(CallType.FLOWER, [41]), Call(CallType.FLOWER, [43])],
        )
        self.assertSequenceEqual(
            game.get_hand(1), [2, 2, 2, 2, 5, 5, 5, 5, 7, 13, 13, 13, 37]
        )
        self.assertSequenceEqual(
            game.get_calls(1),
            [Call(CallType.FLOWER, [42])],
        )
        self.assertSequenceEqual(
            game.get_hand(2), [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32]
        )
        self.assertSequenceEqual(
            game.get_hand(3), [3, 3, 3, 3, 6, 6, 6, 6, 8, 8, 8, 8, 9]
        )

    def test_ron(self):
        game = Game(test_deck2)
        game.discard(0, 13)
        game.ron(2)
        self.assertEqual(game.status, GameStatus.END)
        win_info = game.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 0)
        self.assertSequenceEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 13]
        )
        self.assertSequenceEqual(win_info.calls, [])

    def test_tsumo(self):
        game = Game(test_deck2)
        game.discard(0, 1)
        game.draw(1)
        game.discard(1, 2)
        game.draw(2)
        game.tsumo(2)
        self.assertEqual(game.status, GameStatus.END)
        win_info = game.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, -1)
        self.assertSequenceEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 16]
        )
        self.assertSequenceEqual(win_info.calls, [])

    def test_chankan(self):
        game = Game(test_deck2)
        game.discard(0, 13)
        game.pon(1)
        game.discard(1, 7)
        game.open_kan(0)
        game.discard(0, 1)
        game.draw(1)
        game.add_kan(1, 13)
        game.ron(2)
        self.assertEqual(game.status, GameStatus.END)
        win_info = game.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 1)
        self.assertSequenceEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 13]
        )
        self.assertSequenceEqual(win_info.calls, [])


class AllowedActionTest(unittest.TestCase):

    def test_play_default_actions(self):
        game = Game(test_deck)
        self.assertEqual(
            game.allowed_actions(0).default, Action(ActionType.DISCARD, 21)
        )
        self.assertEqual(game.allowed_actions(1).default, Action(ActionType.NOTHING, 0))
        self.assertEqual(game.allowed_actions(2).default, Action(ActionType.NOTHING, 0))
        self.assertEqual(game.allowed_actions(3).default, Action(ActionType.NOTHING, 0))

    def test_discarded_default_actions(self):
        game = Game(test_deck)
        game.discard(0, 9)
        self.assertEqual(game.allowed_actions(0).default, Action(ActionType.NOTHING, 0))
        self.assertEqual(game.allowed_actions(1).default, Action(ActionType.DRAW, 0))
        self.assertEqual(game.allowed_actions(2).default, Action(ActionType.NOTHING, 0))
        self.assertEqual(game.allowed_actions(3).default, Action(ActionType.NOTHING, 0))

    def test_wrong_turn_nothing(self):
        game = Game(test_deck)
        self.assertSetEqual(
            game.allowed_actions(1).actions, {Action(ActionType.NOTHING, 0)}
        )
        self.assertSetEqual(
            game.allowed_actions(2).actions, {Action(ActionType.NOTHING, 0)}
        )
        self.assertSetEqual(
            game.allowed_actions(3).actions, {Action(ActionType.NOTHING, 0)}
        )

    def test_turn_discard_actions(self):
        game = Game(test_deck)
        self.assertSetEqual(
            game.allowed_actions(0).actions,
            {
                Action(ActionType.DISCARD, 1),
                Action(ActionType.DISCARD, 2),
                Action(ActionType.DISCARD, 3),
                Action(ActionType.DISCARD, 4),
                Action(ActionType.DISCARD, 5),
                Action(ActionType.DISCARD, 6),
                Action(ActionType.DISCARD, 7),
                Action(ActionType.DISCARD, 8),
                Action(ActionType.DISCARD, 9),
                Action(ActionType.DISCARD, 17),
                Action(ActionType.DISCARD, 21),
            },
        )

    def test_discard_self_cannot_chi(self):
        game = Game(test_deck)
        game.discard(0, 1)
        self.assertSetEqual(
            game.allowed_actions(0).actions, {Action(ActionType.NOTHING, 0)}
        )

    def test_discard_self_cannot_pon(self):
        game = Game(test_deck)
        game.discard(0, 21)
        self.assertSetEqual(
            game.allowed_actions(0).actions, {Action(ActionType.NOTHING, 0)}
        )

    def test_can_draw(self):
        game = Game(test_deck)
        game.discard(0, 17)
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {Action(ActionType.DRAW, 0)},
        )

    def test_can_chi_abc(self):
        game = Game(test_deck)
        game.discard(0, 5)
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DRAW, 0),
                Action(ActionType.CHI_A, 5),
                Action(ActionType.CHI_B, 5),
                Action(ActionType.CHI_C, 5),
            },
        )

    def test_can_pon_kan(self):
        game = Game(test_deck)
        game.discard(0, 9)
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DRAW, 0),
                Action(ActionType.CHI_C, 9),
                Action(ActionType.PON, 9),
                Action(ActionType.OPEN_KAN, 9),
            },
        )

    def test_discard_actions_after_chi(self):
        game = Game(test_deck)
        game.discard(0, 9)
        game.chi_c(1)
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DISCARD, 1),
                Action(ActionType.DISCARD, 2),
                Action(ActionType.DISCARD, 3),
                Action(ActionType.DISCARD, 4),
                Action(ActionType.DISCARD, 5),
                Action(ActionType.DISCARD, 6),
                Action(ActionType.DISCARD, 9),
                Action(ActionType.DISCARD, 17),
                Action(ActionType.DISCARD, 21),
            },
        )

    def test_cannot_kan_after_call(self):
        game = Game(test_deck)
        game.discard(0, 9)
        game.pon(1)
        self.assertSetEqual(
            game.allowed_actions(1).actions,
            {
                Action(ActionType.DISCARD, 1),
                Action(ActionType.DISCARD, 2),
                Action(ActionType.DISCARD, 3),
                Action(ActionType.DISCARD, 4),
                Action(ActionType.DISCARD, 5),
                Action(ActionType.DISCARD, 6),
                Action(ActionType.DISCARD, 7),
                Action(ActionType.DISCARD, 8),
                Action(ActionType.DISCARD, 9),
                Action(ActionType.DISCARD, 17),
                Action(ActionType.DISCARD, 21),
            },
        )

    def test_can_ron(self):
        game = Game(test_deck2)
        game.discard(0, 13)
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {Action(ActionType.NOTHING, 0), Action(ActionType.RON, 13)},
        )

    def test_can_tsumo(self):
        game = Game(test_deck2)
        game.discard(0, 1)
        game.draw(1)
        game.discard(1, 2)
        game.draw(2)
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {
                Action(ActionType.DISCARD, 11),
                Action(ActionType.DISCARD, 12),
                Action(ActionType.DISCARD, 14),
                Action(ActionType.DISCARD, 15),
                Action(ActionType.DISCARD, 16),
                Action(ActionType.DISCARD, 31),
                Action(ActionType.DISCARD, 32),
                Action(ActionType.TSUMO, 0),
            },
        )

    def test_cannot_ron_own_discard(self):
        game = Game(test_deck2)
        game.discard(0, 1)
        game.draw(1)
        game.discard(1, 2)
        game.draw(2)
        game.discard(2, 11)
        self.assertSetEqual(
            game.allowed_actions(2).actions, {Action(ActionType.NOTHING, 0)}
        )

    def test_can_chankan(self):
        game = Game(test_deck2)
        game.discard(0, 13)
        game.pon(1)
        game.discard(1, 7)
        game.open_kan(0)
        game.discard(0, 1)
        game.draw(1)
        game.add_kan(1, 13)
        self.assertSetEqual(
            game.allowed_actions(2).actions,
            {Action(ActionType.NOTHING, 0), Action(ActionType.RON, 13)},
        )
