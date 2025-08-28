import unittest

from src.mahjong.game import Game, GameOptions, GameStatus
from src.mahjong.action import Action, ActionType
from src.mahjong.call import Call, CallType

from tests.decks import *


class GameTest(unittest.TestCase):
    def test_start(self):
        game = Game(test_deck1)
        self.assertEqual(game.current_player, 0)
        self.assertEqual(game.status, GameStatus.PLAY)
        self.assertSequenceEqual(game.discard_pool, [])
        self.assertSequenceEqual(
            game.history,
            [
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
            ],
        )

    def test_fixed_deck_start_hands(self):
        game = Game(test_deck1)
        self.assertCountEqual(
            game.get_hand(0), [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21, 21, 21]
        )
        self.assertCountEqual(
            game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21]
        )
        self.assertCountEqual(
            game.get_hand(2), [11, 11, 11, 11, 13, 13, 13, 13, 15, 15, 15, 15, 17]
        )
        self.assertCountEqual(
            game.get_hand(3), [12, 12, 12, 12, 14, 14, 14, 14, 16, 16, 16, 16, 17]
        )

    def test_discard_pool(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=17))
        self.assertSequenceEqual(game.discard_pool, [17])

    def test_discard_hand(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=17))
        self.assertCountEqual(
            game.get_hand(0), [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 21, 21]
        )

    def test_draw(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=17))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        self.assertCountEqual(
            game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21, 1]
        )

    def test_chi_a(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=5))
        game.do_action(1, Action(action_type=ActionType.CHI_A))
        self.assertCountEqual(game.get_hand(1), [1, 2, 3, 4, 5, 8, 9, 9, 9, 17, 21])
        self.assertCountEqual(
            game.get_calls(1), [Call(call_type=CallType.CHI, tiles=[5, 6, 7])]
        )
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_chi_b(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=5))
        game.do_action(1, Action(action_type=ActionType.CHI_B))
        self.assertCountEqual(game.get_hand(1), [1, 2, 3, 5, 7, 8, 9, 9, 9, 17, 21])
        self.assertCountEqual(
            game.get_calls(1), [Call(call_type=CallType.CHI, tiles=[4, 5, 6])]
        )
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_chi_c(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=5))
        game.do_action(1, Action(action_type=ActionType.CHI_C))
        self.assertCountEqual(game.get_hand(1), [1, 2, 5, 6, 7, 8, 9, 9, 9, 17, 21])
        self.assertCountEqual(
            game.get_calls(1), [Call(call_type=CallType.CHI, tiles=[3, 4, 5])]
        )
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_pon(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        game.do_action(1, Action(action_type=ActionType.PON))
        self.assertCountEqual(game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertCountEqual(
            game.get_calls(1), [Call(call_type=CallType.PON, tiles=[9, 9, 9])]
        )
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_pon_change_turn(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        game.do_action(0, Action(action_type=ActionType.PON))
        self.assertCountEqual(game.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertCountEqual(
            game.get_calls(0), [Call(call_type=CallType.PON, tiles=[21, 21, 21])]
        )
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [1, 2])

    def test_open_kan(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        game.do_action(1, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(game.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 17, 21, 8])
        self.assertCountEqual(
            game.get_calls(1), [Call(call_type=CallType.OPEN_KAN, tiles=[9, 9, 9, 9])]
        )
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [2])

    def test_open_kan_change_turn(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        game.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(game.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 8])
        self.assertCountEqual(
            game.get_calls(0),
            [Call(call_type=CallType.OPEN_KAN, tiles=[21, 21, 21, 21])],
        )
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [1, 2])

    def test_add_kan(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        game.do_action(1, Action(action_type=ActionType.PON))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        game.do_action(0, Action(action_type=ActionType.PON))
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=9))
        self.assertCountEqual(game.get_hand(1), [1, 1, 2, 3, 4, 5, 6, 7, 8, 17, 8])
        self.assertCountEqual(
            game.get_calls(1), [Call(call_type=CallType.ADD_KAN, tiles=[9, 9, 9, 9])]
        )
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(game.discard_pool, [1, 2])

    def test_closed_kan(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        game.do_action(2, Action(action_type=ActionType.DRAW))
        game.do_action(2, Action(action_type=ActionType.CLOSED_KAN, tile=11))
        self.assertCountEqual(
            game.get_hand(2), [2, 13, 13, 13, 13, 15, 15, 15, 15, 17, 8]
        )
        self.assertCountEqual(
            game.get_calls(2),
            [Call(call_type=CallType.CLOSED_KAN, tiles=[11, 11, 11, 11])],
        )
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.DISCARD, tile=13))
        self.assertSequenceEqual(game.discard_pool, [1, 2, 13])

    def test_deck_2_start_hands(self):
        game = Game(test_deck2)
        self.assertCountEqual(
            game.get_hand(0), [1, 1, 1, 1, 4, 4, 4, 4, 7, 7, 7, 9, 13, 36]
        )
        self.assertCountEqual(
            game.get_calls(0),
            [
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[43]),
            ],
        )
        self.assertCountEqual(
            game.get_hand(1), [2, 2, 2, 2, 5, 5, 5, 5, 7, 13, 13, 13, 37]
        )
        self.assertCountEqual(
            game.get_calls(1),
            [Call(call_type=CallType.FLOWER, tiles=[42])],
        )
        self.assertCountEqual(
            game.get_hand(2), [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32]
        )
        self.assertCountEqual(game.get_hand(3), [3, 3, 3, 3, 6, 6, 6, 6, 8, 8, 8, 8, 9])

    def test_history(self):
        game = Game(test_deck1)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        game.do_action(1, Action(action_type=ActionType.PON))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        game.do_action(0, Action(action_type=ActionType.PON))
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=9))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(
            game.history,
            [
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
                (0, Action(action_type=ActionType.DISCARD, tile=9)),
                (1, Action(action_type=ActionType.PON)),
                (1, Action(action_type=ActionType.DISCARD, tile=21)),
                (0, Action(action_type=ActionType.PON)),
                (0, Action(action_type=ActionType.DISCARD, tile=1)),
                (1, Action(action_type=ActionType.DRAW)),
                (1, Action(action_type=ActionType.ADD_KAN, tile=9)),
                (1, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.DISCARD, tile=2)),
            ],
        )

    def test_ron(self):
        game = Game(test_deck2)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        game.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(game.status, GameStatus.END)
        win_info = game.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 0)
        self.assertCountEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 13]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_tsumo(self):
        game = Game(test_deck2)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        game.do_action(2, Action(action_type=ActionType.DRAW))
        game.do_action(2, Action(action_type=ActionType.TSUMO))
        self.assertEqual(game.status, GameStatus.END)
        win_info = game.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, -1)
        self.assertCountEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 16]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_chankan(self):
        game = Game(test_deck2)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        game.do_action(1, Action(action_type=ActionType.PON))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=7))
        game.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=13))
        game.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(game.status, GameStatus.END)
        win_info = game.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 1)
        self.assertCountEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 13]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_auto_flower_history(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=True))
        self.assertSequenceEqual(
            game.history,
            [
                (0, Action(action_type=ActionType.FLOWER, tile=41)),
                (0, Action(action_type=ActionType.FLOWER, tile=43)),
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.FLOWER, tile=42)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
                (0, Action(action_type=ActionType.FLOWER, tile=44)),
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
            ],
        )

    def test_manual_flower_start(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        self.assertEqual(game.status, GameStatus.START)

    def test_start_flower_call(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        self.assertCountEqual(
            game.get_calls(0), [Call(call_type=CallType.FLOWER, tiles=[41])]
        )

    def test_start_flower_calls(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        self.assertCountEqual(
            game.get_calls(0),
            [
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[43]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
            ],
        )

    def test_start_flower_next_player(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        self.assertCountEqual(
            game.get_hand(1), [2, 2, 2, 2, 6, 6, 6, 6, 12, 12, 12, 12, 35]
        )
        self.assertCountEqual(
            game.get_calls(1), [Call(call_type=CallType.FLOWER, tiles=[42])]
        )

    def test_start_flower_pass_all(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(3, Action(action_type=ActionType.NOTHING))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        self.assertEqual(game.current_player, 0)
        self.assertEqual(game.status, GameStatus.PLAY)

    def test_start_flower_loop_pass_all(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(3, Action(action_type=ActionType.NOTHING))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(3, Action(action_type=ActionType.NOTHING))
        self.assertEqual(game.current_player, 0)
        self.assertEqual(game.status, GameStatus.PLAY)

    def test_draw_flower(self):
        game = Game(test_deck3, GameOptions(auto_replace_flowers=False))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(3, Action(action_type=ActionType.NOTHING))
        game.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        game.do_action(0, Action(action_type=ActionType.NOTHING))
        game.do_action(1, Action(action_type=ActionType.NOTHING))
        game.do_action(2, Action(action_type=ActionType.NOTHING))
        game.do_action(3, Action(action_type=ActionType.NOTHING))
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        game.do_action(2, Action(action_type=ActionType.DRAW))
        game.do_action(2, Action(action_type=ActionType.FLOWER, tile=45))
        self.assertCountEqual(
            game.get_calls(2), [Call(call_type=CallType.FLOWER, tiles=[45])]
        )
        self.assertCountEqual(
            game.get_hand(2), [3, 3, 3, 3, 7, 7, 7, 7, 9, 13, 13, 13, 13, 46]
        )

    def test_deck4_start_hands(self):
        game = Game(test_deck4)
        self.assertCountEqual(
            game.get_hand(0), [13, 1, 1, 1, 4, 4, 4, 4, 7, 7, 7, 7, 31, 32]
        )
        self.assertCountEqual(
            game.get_hand(1), [11, 12, 2, 2, 5, 5, 5, 5, 8, 8, 8, 8, 31]
        )
        self.assertCountEqual(
            game.get_hand(2), [13, 13, 3, 3, 6, 6, 6, 6, 9, 9, 9, 9, 31]
        )
        self.assertCountEqual(
            game.get_hand(3), [21, 21, 21, 21, 22, 22, 22, 22, 23, 23, 23, 23, 13]
        )

    def test_priority(self):
        game = Game(test_deck4)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        actions = [
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.PON),
            Action(action_type=ActionType.RON),
        ]
        player, action = game.get_priority_action(actions)
        self.assertEqual(player, 3)
        self.assertEqual(action, Action(action_type=ActionType.RON))

    def test_priority_bad_action(self):
        game = Game(test_deck4)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        actions = [
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.RON),
            Action(action_type=ActionType.NOTHING),
        ]
        player, action = game.get_priority_action(actions)
        self.assertEqual(player, 1)
        self.assertEqual(action, Action(action_type=ActionType.CHI_C))

    def test_priority_current_player(self):
        game = Game(test_deck4)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        game.do_action(1, Action(action_type=ActionType.DRAW))
        game.do_action(1, Action(action_type=ActionType.CLOSED_KAN, tile=5))
        actions = [
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.NOTHING),
        ]
        player, action = game.get_priority_action(actions)
        self.assertEqual(player, 1)
        self.assertEqual(action, Action(action_type=ActionType.NOTHING))

    def test_use_all_tiles(self):
        game = Game(test_deck4, GameOptions(end_wall_count=14))
        while game.status != GameStatus.END:
            actions = [game.allowed_actions(player).default for player in range(4)]
            player, action = game.get_priority_action(actions)
            game.do_action(player, action)
        self.assertEqual(game.wall_count, 14)
        self.assertIsNone(game.win_info)

    def test_houtei(self):
        game = Game(test_deck4, GameOptions(end_wall_count=14))
        game.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=4))
        while game.wall_count > 14:
            actions = [game.allowed_actions(player).default for player in range(4)]
            player, action = game.get_priority_action(actions)
            game.do_action(player, action)
        self.assertEqual(game.current_player, 0)
        self.assertEqual(game.status, GameStatus.PLAY)
        game.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        self.assertEqual(game.status, GameStatus.LAST_DISCARDED)
        game.do_action(3, Action(action_type=ActionType.RON))
        self.assertIsNotNone(game.win_info)
