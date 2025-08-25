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
        game.do_action(0, Action(ActionType.DISCARD, 17))
        self.assertSequenceEqual(game.discard_pool, [17])

    def test_discard_hand(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 17))
        self.assertSequenceEqual(
            game.get_hand(0), [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 21, 21]
        )

    def test_draw(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 17))
        game.do_action(1, Action(ActionType.DRAW))
        self.assertSequenceEqual(
            game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21, 1]
        )

    def test_chi_a(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 5))
        game.do_action(1, Action(ActionType.CHI_A))
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 4, 5, 8, 9, 9, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.CHI, [5, 6, 7])])
        game.do_action(1, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_chi_b(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 5))
        game.do_action(1, Action(ActionType.CHI_B))
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 5, 7, 8, 9, 9, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.CHI, [4, 5, 6])])
        game.do_action(1, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_chi_c(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 5))
        game.do_action(1, Action(ActionType.CHI_C))
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 5, 6, 7, 8, 9, 9, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.CHI, [3, 4, 5])])
        game.do_action(1, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_pon(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 9))
        game.do_action(1, Action(ActionType.PON))
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(1), [Call(CallType.PON, [9, 9, 9])])
        game.do_action(1, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_pon_change_turn(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.DISCARD, 21))
        game.do_action(0, Action(ActionType.PON))
        self.assertSequenceEqual(game.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertSequenceEqual(game.get_calls(0), [Call(CallType.PON, [21, 21, 21])])
        game.do_action(0, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [1, 2])

    def test_open_kan(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 9))
        game.do_action(1, Action(ActionType.OPEN_KAN))
        self.assertSequenceEqual(game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 17, 21, 8])
        self.assertSequenceEqual(
            game.get_calls(1), [Call(CallType.OPEN_KAN, [9, 9, 9, 9])]
        )
        game.do_action(1, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_open_kan_change_turn(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.DISCARD, 21))
        game.do_action(0, Action(ActionType.OPEN_KAN))
        self.assertSequenceEqual(game.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 8])
        self.assertSequenceEqual(
            game.get_calls(0), [Call(CallType.OPEN_KAN, [21, 21, 21, 21])]
        )
        game.do_action(0, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [1, 2])

    def test_add_kan(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 9))
        game.do_action(1, Action(ActionType.PON))
        game.do_action(1, Action(ActionType.DISCARD, 21))
        game.do_action(0, Action(ActionType.PON))
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.ADD_KAN, 9))
        self.assertSequenceEqual(game.get_hand(1), [1, 1, 2, 3, 4, 5, 6, 7, 8, 17, 8])
        self.assertSequenceEqual(
            game.get_calls(1), [Call(CallType.ADD_KAN, [9, 9, 9, 9])]
        )
        game.do_action(1, Action(ActionType.NOTHING))
        game.do_action(1, Action(ActionType.DISCARD, 2))
        self.assertSequenceEqual(game.discard_pool, [1, 2])

    def test_closed_kan(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.DISCARD, 2))
        game.do_action(2, Action(ActionType.DRAW))
        game.do_action(2, Action(ActionType.CLOSED_KAN, 11))
        self.assertSequenceEqual(
            game.get_hand(2), [2, 13, 13, 13, 13, 15, 15, 15, 15, 17, 8]
        )
        self.assertSequenceEqual(
            game.get_calls(2), [Call(CallType.CLOSED_KAN, [11, 11, 11, 11])]
        )
        game.do_action(2, Action(ActionType.NOTHING))
        game.do_action(2, Action(ActionType.DISCARD, 13))
        self.assertSequenceEqual(game.discard_pool, [1, 2, 13])

    def test_discard_sort(self):
        game = Game(test_deck)
        game.do_action(0, Action(ActionType.DISCARD, 17))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.DISCARD, 3))
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
        game.do_action(0, Action(ActionType.DISCARD, 13))
        game.do_action(2, Action(ActionType.RON))
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
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.DISCARD, 2))
        game.do_action(2, Action(ActionType.DRAW))
        game.do_action(2, Action(ActionType.TSUMO))
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
        game.do_action(0, Action(ActionType.DISCARD, 13))
        game.do_action(1, Action(ActionType.PON))
        game.do_action(1, Action(ActionType.DISCARD, 7))
        game.do_action(0, Action(ActionType.OPEN_KAN))
        game.do_action(0, Action(ActionType.DISCARD, 1))
        game.do_action(1, Action(ActionType.DRAW))
        game.do_action(1, Action(ActionType.ADD_KAN, 13))
        game.do_action(2, Action(ActionType.RON))
        self.assertEqual(game.status, GameStatus.END)
        win_info = game.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 1)
        self.assertSequenceEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 13]
        )
        self.assertSequenceEqual(win_info.calls, [])
