import unittest

from src.mahjong.round import Round, RoundStatus
from src.mahjong.action import Action, ActionType
from src.mahjong.call import Call, CallType
from src.mahjong.game_options import GameOptions

from tests.decks import *


class RoundTest(unittest.TestCase):
    def test_start(self):
        round = Round(tiles=test_deck1)
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)
        self.assertSequenceEqual(round.discard_tiles, [])
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
            ],
        )

    def test_fixed_deck_start_hands(self):
        round = Round(tiles=test_deck1)
        self.assertCountEqual(
            round.get_hand(0),
            [10, 20, 30, 40, 50, 60, 70, 80, 90, 210, 211, 212, 170, 12],
        )
        self.assertCountEqual(
            round.get_hand(1), [11, 21, 31, 41, 51, 61, 71, 81, 91, 92, 93, 213, 171]
        )
        self.assertCountEqual(
            round.get_hand(2),
            [110, 111, 112, 113, 130, 131, 132, 133, 150, 151, 152, 153, 172],
        )
        self.assertCountEqual(
            round.get_hand(3),
            [120, 121, 122, 123, 140, 141, 142, 143, 160, 161, 162, 163, 173],
        )

    def test_sub_round_start_hands(self):
        round = Round(tiles=test_deck1, sub_round=1)
        self.assertCountEqual(
            round.get_hand(1),
            [10, 20, 30, 40, 50, 60, 70, 80, 90, 210, 211, 212, 170, 12],
        )
        self.assertCountEqual(
            round.get_hand(2), [11, 21, 31, 41, 51, 61, 71, 81, 91, 92, 93, 213, 171]
        )
        self.assertCountEqual(
            round.get_hand(3),
            [110, 111, 112, 113, 130, 131, 132, 133, 150, 151, 152, 153, 172],
        )
        self.assertCountEqual(
            round.get_hand(0),
            [120, 121, 122, 123, 140, 141, 142, 143, 160, 161, 162, 163, 173],
        )

    def test_discard_pool(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=170))
        self.assertSequenceEqual(round.discard_tiles, [170])

    def test_discard_hand(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=170))
        self.assertCountEqual(
            round.get_hand(0), [10, 12, 20, 30, 40, 50, 60, 70, 80, 90, 210, 211, 212]
        )

    def test_draw(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=170))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        self.assertCountEqual(
            round.get_hand(1),
            [11, 21, 31, 41, 51, 61, 71, 81, 91, 92, 93, 213, 171, 13],
        )

    def test_chi_a(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=50))
        round.do_action(1, Action(action_type=ActionType.CHI_A))
        self.assertCountEqual(
            round.get_hand(1), [11, 21, 31, 41, 51, 81, 91, 92, 93, 213, 171]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[50, 61, 71])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSequenceEqual(round.discard_tiles, [21])

    def test_chi_b(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=50))
        round.do_action(1, Action(action_type=ActionType.CHI_B))
        self.assertCountEqual(
            round.get_hand(1), [11, 21, 31, 51, 71, 81, 91, 92, 93, 213, 171]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[41, 50, 61])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSequenceEqual(round.discard_tiles, [21])

    def test_chi_c(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=50))
        round.do_action(1, Action(action_type=ActionType.CHI_C))
        self.assertCountEqual(
            round.get_hand(1), [11, 21, 51, 61, 71, 81, 91, 92, 93, 213, 171]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[31, 41, 50])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSequenceEqual(round.discard_tiles, [21])

    def test_pon(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        round.do_action(1, Action(action_type=ActionType.PON))
        self.assertCountEqual(
            round.get_hand(1), [11, 21, 31, 41, 51, 61, 71, 81, 93, 213, 171]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.PON, tiles=[90, 91, 92])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSequenceEqual(round.discard_tiles, [21])

    def test_pon_change_turn(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=213))
        round.do_action(0, Action(action_type=ActionType.PON))
        self.assertCountEqual(
            round.get_hand(0), [20, 30, 40, 50, 60, 70, 80, 90, 212, 170, 12]
        )
        self.assertCountEqual(
            round.get_calls(0), [Call(call_type=CallType.PON, tiles=[213, 210, 211])]
        )
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=20))
        self.assertSequenceEqual(round.discard_tiles, [10, 20])

    def test_open_kan(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        round.do_action(1, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(
            round.get_hand(1), [11, 21, 31, 41, 51, 61, 71, 81, 213, 171, 83]
        )
        self.assertCountEqual(
            round.get_calls(1),
            [Call(call_type=CallType.OPEN_KAN, tiles=[90, 91, 92, 93])],
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSequenceEqual(round.discard_tiles, [21])

    def test_open_kan_change_turn(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=213))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(
            round.get_hand(0), [20, 30, 40, 50, 60, 70, 80, 90, 170, 12, 83]
        )
        self.assertCountEqual(
            round.get_calls(0),
            [Call(call_type=CallType.OPEN_KAN, tiles=[213, 210, 211, 212])],
        )
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=20))
        self.assertSequenceEqual(round.discard_tiles, [10, 20])

    def test_add_kan(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=213))
        round.do_action(0, Action(action_type=ActionType.PON))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=93))
        self.assertCountEqual(
            round.get_hand(1), [11, 13, 21, 31, 41, 51, 61, 71, 81, 171, 83]
        )
        self.assertCountEqual(
            round.get_calls(1),
            [Call(call_type=CallType.ADD_KAN, tiles=[93, 90, 91, 92])],
        )
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSequenceEqual(round.discard_tiles, [10, 21])

    def test_closed_kan(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.CLOSED_KAN, tile=110))
        self.assertCountEqual(
            round.get_hand(2), [22, 130, 131, 132, 133, 150, 151, 152, 153, 172, 83]
        )
        self.assertCountEqual(
            round.get_calls(2),
            [Call(call_type=CallType.CLOSED_KAN, tiles=[110, 111, 112, 113])],
        )
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.DISCARD, tile=130))
        self.assertSequenceEqual(round.discard_tiles, [10, 21, 130])

    def test_deck_2_start_hands(self):
        round = Round(tiles=test_deck2)
        self.assertCountEqual(
            round.get_hand(0),
            [10, 11, 12, 13, 40, 41, 42, 43, 70, 71, 72, 130, 91, 360],
        )
        self.assertCountEqual(round.get_calls(0), [])
        self.assertCountEqual(round.get_flowers(0), [410, 430])
        self.assertCountEqual(
            round.get_hand(1), [20, 21, 22, 23, 50, 51, 52, 53, 73, 131, 132, 133, 370]
        )
        self.assertCountEqual(round.get_calls(1), [])
        self.assertCountEqual(round.get_flowers(1), [420])
        self.assertCountEqual(
            round.get_hand(2),
            [110, 111, 112, 120, 121, 122, 310, 311, 320, 321, 322, 140, 150],
        )
        self.assertCountEqual(
            round.get_hand(3), [30, 31, 32, 33, 60, 61, 62, 63, 80, 81, 82, 83, 90]
        )

    def test_history(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=90))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=213))
        round.do_action(0, Action(action_type=ActionType.PON))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=93))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=21))
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.DISCARD, tile=90)),
                (1, Action(action_type=ActionType.PON)),
                (1, Action(action_type=ActionType.DISCARD, tile=213)),
                (0, Action(action_type=ActionType.PON)),
                (0, Action(action_type=ActionType.DISCARD, tile=10)),
                (1, Action(action_type=ActionType.DRAW)),
                (1, Action(action_type=ActionType.ADD_KAN, tile=93)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.DISCARD, tile=21)),
            ],
        )

    def test_ron(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        round.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 0)
        self.assertCountEqual(
            win_info.hand,
            [110, 111, 112, 120, 121, 122, 310, 311, 320, 321, 322, 140, 150, 130],
        )
        self.assertCountEqual(win_info.calls, [])

    def test_tsumo(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.TSUMO))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, None)
        self.assertCountEqual(
            win_info.hand,
            [110, 111, 112, 120, 121, 122, 310, 311, 320, 321, 322, 140, 150, 160],
        )
        self.assertCountEqual(win_info.calls, [])

    def test_chankan(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=73))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=133))
        round.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 1)
        self.assertCountEqual(
            win_info.hand,
            [110, 111, 112, 120, 121, 122, 310, 311, 320, 321, 322, 140, 150, 133],
        )
        self.assertCountEqual(win_info.calls, [])
        self.assertTrue(win_info.is_chankan)

    def test_auto_flower_history(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=True))
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.FLOWER, tile=410)),
                (0, Action(action_type=ActionType.FLOWER, tile=430)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.FLOWER, tile=420)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.FLOWER, tile=440)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
            ],
        )

    def test_sub_round_auto_flower_history(self):
        round = Round(
            tiles=test_deck3,
            sub_round=1,
            options=GameOptions(auto_replace_flowers=True),
        )
        self.assertSequenceEqual(
            round.history,
            [
                (1, Action(action_type=ActionType.FLOWER, tile=410)),
                (1, Action(action_type=ActionType.FLOWER, tile=430)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.FLOWER, tile=420)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.FLOWER, tile=440)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
            ],
        )

    def test_auto_flower_one_person_draw_flower(self):
        round = Round(tiles=test_deck5, options=GameOptions(auto_replace_flowers=True))
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.FLOWER, tile=410)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.FLOWER, tile=420)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
            ],
        )

    def test_manual_flower_start(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        self.assertEqual(round.status, RoundStatus.START)

    def test_start_flower_call(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=410))
        self.assertCountEqual(round.get_flowers(0), [410])

    def test_start_flower_calls(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=440))
        self.assertCountEqual(round.get_flowers(0), [410, 430, 440])

    def test_start_flower_next_player(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=420))
        self.assertCountEqual(
            round.get_hand(1), [20, 21, 22, 23, 60, 61, 62, 63, 120, 121, 122, 123, 350]
        )
        self.assertCountEqual(round.get_flowers(1), [420])

    def test_start_flower_pass_all(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)

    def test_start_flower_loop_pass_all(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)

    def test_draw_flower(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=410))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=430))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=420))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=440))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.FLOWER, tile=450))
        self.assertCountEqual(round.get_flowers(2), [450])
        self.assertCountEqual(
            round.get_hand(2),
            [30, 31, 32, 33, 70, 71, 72, 73, 130, 131, 132, 133, 90, 460],
        )

    def test_priority(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        actions = [
            Action(action_type=ActionType.PASS),
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.PON),
            Action(action_type=ActionType.RON),
        ]
        player, action = round.get_priority_action(actions)
        self.assertEqual(player, 3)
        self.assertEqual(action, Action(action_type=ActionType.RON))

    def test_priority_with_none(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        actions = [
            None,
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.PON),
            Action(action_type=ActionType.RON),
        ]
        player, action = round.get_priority_action(actions)
        self.assertEqual(player, 3)
        self.assertEqual(action, Action(action_type=ActionType.RON))

    def test_priority_strong_call_and_none(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        actions = [
            None,
            None,
            None,
            Action(action_type=ActionType.RON),
        ]
        player, action = round.get_priority_action(actions)
        self.assertEqual(player, 3)
        self.assertEqual(action, Action(action_type=ActionType.RON))

    def test_priority_weak_call_and_none(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        actions = [
            None,
            Action(action_type=ActionType.CHI_C),
            None,
            None,
        ]
        playeraction = round.get_priority_action(actions)
        self.assertEqual(playeraction, None)

    def test_priority_no_choice_all_none(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=10))
        actions = [
            None,
            None,
            None,
            None,
        ]
        player, action = round.get_priority_action(actions)
        self.assertEqual(player, 1)
        self.assertEqual(action, Action(action_type=ActionType.DRAW))

    def test_priority_bad_action(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        actions = [
            Action(action_type=ActionType.PASS),
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.RON),
            Action(action_type=ActionType.PASS),
        ]
        player, action = round.get_priority_action(actions)
        self.assertEqual(player, 1)
        self.assertEqual(action, Action(action_type=ActionType.CHI_C))

    def test_priority_bad_action_and_none(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        actions = [
            None,
            Action(action_type=ActionType.CHI_C),
            Action(action_type=ActionType.PON),
            Action(action_type=ActionType.OPEN_KAN),
        ]
        player, action = round.get_priority_action(actions)
        self.assertEqual(player, 2)
        self.assertEqual(action, Action(action_type=ActionType.PON))

    def test_priority_current_player(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.CLOSED_KAN, tile=50))
        actions = [
            Action(action_type=ActionType.PASS),
            Action(action_type=ActionType.CONTINUE),
            Action(action_type=ActionType.PASS),
            Action(action_type=ActionType.PASS),
        ]
        player, action = round.get_priority_action(actions)
        self.assertEqual(player, 1)
        self.assertEqual(action, Action(action_type=ActionType.CONTINUE))

    def test_use_all_tiles(self):
        round = Round(tiles=test_deck4, options=GameOptions(end_wall_count=14))
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(round.wall_count, 14)
        self.assertIsNone(round.win_info)

    def test_haitei(self):
        round = Round(tiles=test_deck_haitei, options=GameOptions(end_wall_count=14))
        while round.wall_count > 14:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(round.current_player, 1)
        self.assertEqual(round.status, RoundStatus.PLAY)
        round.do_action(1, Action(action_type=ActionType.TSUMO))
        self.assertIsNotNone(round.win_info)
        self.assertTrue(round.win_info.is_haitei)

    def test_houtei(self):
        round = Round(tiles=test_deck4, options=GameOptions(end_wall_count=14))
        round.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=40))
        while round.wall_count > 14:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=130))
        self.assertEqual(round.status, RoundStatus.LAST_DISCARDED)
        round.do_action(3, Action(action_type=ActionType.RON))
        self.assertIsNotNone(round.win_info)
        self.assertTrue(round.win_info.is_houtei)

    def test_after_flower(self):
        round = Round(tiles=test_deck_rinshan)
        round.do_action(0, Action(action_type=ActionType.TSUMO))
        win = round.win_info
        self.assertEqual(win.after_flower_count, 5)

    def test_after_flower_and_kan(self):
        round = Round(tiles=test_deck_rinshan)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=110))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.CLOSED_KAN, tile=10))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=480))
        round.do_action(1, Action(action_type=ActionType.TSUMO))
        win = round.win_info
        self.assertEqual(win.after_flower_count, 1)
        self.assertEqual(win.after_kan_count, 1)

    def test_tenhou(self):
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, Action(action_type=ActionType.TSUMO))
        self.assertTrue(round.win_info.is_tenhou)

    def test_sub_round_tenhou(self):
        round = Round(tiles=test_deck_kan_tenhou, sub_round=1)
        round.do_action(1, Action(action_type=ActionType.TSUMO))
        self.assertTrue(round.win_info.is_tenhou)

    def test_not_tenhou_after_call(self):
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=160))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.TSUMO))
        self.assertFalse(round.win_info.is_tenhou)

    def test_chiihou(self):
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=110))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.TSUMO))
        self.assertTrue(round.win_info.is_chiihou)

    def test_not_chiihou_after_call(self):
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=160))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=110))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.TSUMO))
        self.assertFalse(round.win_info.is_chiihou)
