import unittest

from src.mahjong.round import Round, RoundStatus
from src.mahjong.action import Action, ActionType
from src.mahjong.call import Call, CallType
from src.mahjong.game_options import GameOptions

from tests.decks import *


class RoundTest(unittest.TestCase):
    def test_start(self):
        round = Round(test_deck1)
        self.assertEqual(round.current_seat, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)
        self.assertSequenceEqual(round.discard_pool, [])
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
                (0, Action(action_type=ActionType.NOTHING)),
            ],
        )

    def test_fixed_deck_start_hands(self):
        round = Round(test_deck1)
        self.assertCountEqual(
            round.get_hand(0), [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21, 21, 21]
        )
        self.assertCountEqual(
            round.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21]
        )
        self.assertCountEqual(
            round.get_hand(2), [11, 11, 11, 11, 13, 13, 13, 13, 15, 15, 15, 15, 17]
        )
        self.assertCountEqual(
            round.get_hand(3), [12, 12, 12, 12, 14, 14, 14, 14, 16, 16, 16, 16, 17]
        )

    def test_discard_pool(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=17))
        self.assertSequenceEqual(round.discard_pool, [17])

    def test_discard_hand(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=17))
        self.assertCountEqual(
            round.get_hand(0), [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 21, 21]
        )

    def test_draw(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=17))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        self.assertCountEqual(
            round.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 17, 21, 1]
        )

    def test_chi_a(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=5))
        round.do_action(1, Action(action_type=ActionType.CHI_A))
        self.assertCountEqual(round.get_hand(1), [1, 2, 3, 4, 5, 8, 9, 9, 9, 17, 21])
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[5, 6, 7])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [2])

    def test_chi_b(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=5))
        round.do_action(1, Action(action_type=ActionType.CHI_B))
        self.assertCountEqual(round.get_hand(1), [1, 2, 3, 5, 7, 8, 9, 9, 9, 17, 21])
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[4, 5, 6])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [2])

    def test_chi_c(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=5))
        round.do_action(1, Action(action_type=ActionType.CHI_C))
        self.assertCountEqual(round.get_hand(1), [1, 2, 5, 6, 7, 8, 9, 9, 9, 17, 21])
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[3, 4, 5])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [2])

    def test_pon(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        round.do_action(1, Action(action_type=ActionType.PON))
        self.assertCountEqual(round.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.PON, tiles=[9, 9, 9])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [2])

    def test_pon_change_turn(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        round.do_action(0, Action(action_type=ActionType.PON))
        self.assertCountEqual(round.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 21])
        self.assertCountEqual(
            round.get_calls(0), [Call(call_type=CallType.PON, tiles=[21, 21, 21])]
        )
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [1, 2])

    def test_open_kan(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        round.do_action(1, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(round.get_hand(1), [1, 2, 3, 4, 5, 6, 7, 8, 17, 21, 8])
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.OPEN_KAN, tiles=[9, 9, 9, 9])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [2])

    def test_open_kan_change_turn(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(round.get_hand(0), [1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 8])
        self.assertCountEqual(
            round.get_calls(0),
            [Call(call_type=CallType.OPEN_KAN, tiles=[21, 21, 21, 21])],
        )
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [1, 2])

    def test_add_kan(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        round.do_action(0, Action(action_type=ActionType.PON))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=9))
        self.assertCountEqual(round.get_hand(1), [1, 1, 2, 3, 4, 5, 6, 7, 8, 17, 8])
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.ADD_KAN, tiles=[9, 9, 9, 9])]
        )
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(round.discard_pool, [1, 2])

    def test_closed_kan(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.CLOSED_KAN, tile=11))
        self.assertCountEqual(
            round.get_hand(2), [2, 13, 13, 13, 13, 15, 15, 15, 15, 17, 8]
        )
        self.assertCountEqual(
            round.get_calls(2),
            [Call(call_type=CallType.CLOSED_KAN, tiles=[11, 11, 11, 11])],
        )
        round.do_action(2, Action(action_type=ActionType.NOTHING))
        round.do_action(2, Action(action_type=ActionType.DISCARD, tile=13))
        self.assertSequenceEqual(round.discard_pool, [1, 2, 13])

    def test_deck_2_start_hands(self):
        round = Round(test_deck2)
        self.assertCountEqual(
            round.get_hand(0), [1, 1, 1, 1, 4, 4, 4, 4, 7, 7, 7, 9, 13, 36]
        )
        self.assertCountEqual(
            round.get_calls(0),
            [
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[43]),
            ],
        )
        self.assertCountEqual(
            round.get_hand(1), [2, 2, 2, 2, 5, 5, 5, 5, 7, 13, 13, 13, 37]
        )
        self.assertCountEqual(
            round.get_calls(1),
            [Call(call_type=CallType.FLOWER, tiles=[42])],
        )
        self.assertCountEqual(
            round.get_hand(2), [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32]
        )
        self.assertCountEqual(
            round.get_hand(3), [3, 3, 3, 3, 6, 6, 6, 6, 8, 8, 8, 8, 9]
        )

    def test_history(self):
        round = Round(test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=9))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        round.do_action(0, Action(action_type=ActionType.PON))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=9))
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
                (0, Action(action_type=ActionType.NOTHING)),
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
        round = Round(test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        round.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_seat, 2)
        self.assertEqual(win_info.lose_seat, 0)
        self.assertCountEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 13]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_tsumo(self):
        round = Round(test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.TSUMO))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_seat, 2)
        self.assertEqual(win_info.lose_seat, None)
        self.assertCountEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 16]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_chankan(self):
        round = Round(test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=7))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=13))
        round.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_seat, 2)
        self.assertEqual(win_info.lose_seat, 1)
        self.assertCountEqual(
            win_info.hand, [11, 11, 11, 12, 12, 12, 14, 15, 31, 31, 32, 32, 32, 13]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_auto_flower_history(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=True))
        self.assertSequenceEqual(
            round.history,
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
                (0, Action(action_type=ActionType.NOTHING)),
            ],
        )

    def test_auto_flower_one_person_draw_flower(self):
        round = Round(test_deck5, GameOptions(auto_replace_flowers=True))
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.FLOWER, tile=41)),
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
                (0, Action(action_type=ActionType.FLOWER, tile=42)),
                (0, Action(action_type=ActionType.NOTHING)),
                (1, Action(action_type=ActionType.NOTHING)),
                (2, Action(action_type=ActionType.NOTHING)),
                (3, Action(action_type=ActionType.NOTHING)),
                (0, Action(action_type=ActionType.NOTHING)),
            ],
        )

    def test_manual_flower_start(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=False))
        self.assertEqual(round.status, RoundStatus.START)

    def test_start_flower_call(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        self.assertCountEqual(
            round.get_calls(0), [Call(call_type=CallType.FLOWER, tiles=[41])]
        )

    def test_start_flower_calls(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        self.assertCountEqual(
            round.get_calls(0),
            [
                Call(call_type=CallType.FLOWER, tiles=[41]),
                Call(call_type=CallType.FLOWER, tiles=[43]),
                Call(call_type=CallType.FLOWER, tiles=[44]),
            ],
        )

    def test_start_flower_next_seat(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        self.assertCountEqual(
            round.get_hand(1), [2, 2, 2, 2, 6, 6, 6, 6, 12, 12, 12, 12, 35]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.FLOWER, tiles=[42])]
        )

    def test_start_flower_pass_all(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        round.do_action(2, Action(action_type=ActionType.NOTHING))
        round.do_action(3, Action(action_type=ActionType.NOTHING))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        self.assertEqual(round.current_seat, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)

    def test_start_flower_loop_pass_all(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        round.do_action(2, Action(action_type=ActionType.NOTHING))
        round.do_action(3, Action(action_type=ActionType.NOTHING))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        round.do_action(2, Action(action_type=ActionType.NOTHING))
        round.do_action(3, Action(action_type=ActionType.NOTHING))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        self.assertEqual(round.current_seat, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)

    def test_draw_flower(self):
        round = Round(test_deck3, GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=41))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=43))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=42))
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        round.do_action(2, Action(action_type=ActionType.NOTHING))
        round.do_action(3, Action(action_type=ActionType.NOTHING))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=44))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(1, Action(action_type=ActionType.NOTHING))
        round.do_action(2, Action(action_type=ActionType.NOTHING))
        round.do_action(3, Action(action_type=ActionType.NOTHING))
        round.do_action(0, Action(action_type=ActionType.NOTHING))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=1))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=2))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.FLOWER, tile=45))
        self.assertCountEqual(
            round.get_calls(2), [Call(call_type=CallType.FLOWER, tiles=[45])]
        )
        self.assertCountEqual(
            round.get_hand(2), [3, 3, 3, 3, 7, 7, 7, 7, 9, 13, 13, 13, 13, 46]
        )

    def test_deck4_start_hands(self):
        round = Round(test_deck4)
        self.assertCountEqual(
            round.get_hand(0), [13, 1, 1, 1, 4, 4, 4, 4, 7, 7, 7, 7, 31, 32]
        )
        self.assertCountEqual(
            round.get_hand(1), [11, 12, 2, 2, 5, 5, 5, 5, 8, 8, 8, 8, 31]
        )
        self.assertCountEqual(
            round.get_hand(2), [13, 13, 3, 3, 6, 6, 6, 6, 9, 9, 9, 9, 31]
        )
        self.assertCountEqual(
            round.get_hand(3), [21, 21, 21, 21, 22, 22, 22, 22, 23, 23, 23, 23, 13]
        )

    def test_priority(self):
        round = Round(test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        actions = [
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.PON),
            Action(action_type=ActionType.RON),
        ]
        seat, action = round.get_priority_action(actions)
        self.assertEqual(seat, 3)
        self.assertEqual(action, Action(action_type=ActionType.RON))

    def test_priority_bad_action(self):
        round = Round(test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        actions = [
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.RON),
            Action(action_type=ActionType.NOTHING),
        ]
        seat, action = round.get_priority_action(actions)
        self.assertEqual(seat, 1)
        self.assertEqual(action, Action(action_type=ActionType.CHI_C))

    def test_priority_current_seat(self):
        round = Round(test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.CLOSED_KAN, tile=5))
        actions = [
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.NOTHING),
            Action(action_type=ActionType.NOTHING),
        ]
        seat, action = round.get_priority_action(actions)
        self.assertEqual(seat, 1)
        self.assertEqual(action, Action(action_type=ActionType.NOTHING))

    def test_use_all_tiles(self):
        round = Round(test_deck4, GameOptions(end_wall_count=14))
        while round.status != RoundStatus.END:
            actions = [round.allowed_actions(seat).default for seat in range(4)]
            seat, action = round.get_priority_action(actions)
            round.do_action(seat, action)
        self.assertEqual(round.wall_count, 14)
        self.assertIsNone(round.win_info)

    def test_houtei(self):
        round = Round(test_deck4, GameOptions(end_wall_count=14))
        round.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=4))
        while round.wall_count > 14:
            actions = [round.allowed_actions(seat).default for seat in range(4)]
            seat, action = round.get_priority_action(actions)
            round.do_action(seat, action)
        self.assertEqual(round.current_seat, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=13))
        self.assertEqual(round.status, RoundStatus.LAST_DISCARDED)
        round.do_action(3, Action(action_type=ActionType.RON))
        self.assertIsNotNone(round.win_info)
