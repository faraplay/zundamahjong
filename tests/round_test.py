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
            round.get_hand(0), [4, 8, 12, 16, 20, 24, 28, 32, 36, 84, 85, 86, 68, 6]
        )
        self.assertCountEqual(
            round.get_hand(1), [5, 9, 13, 17, 21, 25, 29, 33, 37, 38, 39, 87, 69]
        )
        self.assertCountEqual(
            round.get_hand(2), [44, 45, 46, 47, 52, 53, 54, 55, 60, 61, 62, 63, 70]
        )
        self.assertCountEqual(
            round.get_hand(3), [48, 49, 50, 51, 56, 57, 58, 59, 64, 65, 66, 67, 71]
        )

    def test_sub_round_start_hands(self):
        round = Round(tiles=test_deck1, sub_round=1)
        self.assertCountEqual(
            round.get_hand(1), [4, 8, 12, 16, 20, 24, 28, 32, 36, 84, 85, 86, 68, 6]
        )
        self.assertCountEqual(
            round.get_hand(2), [5, 9, 13, 17, 21, 25, 29, 33, 37, 38, 39, 87, 69]
        )
        self.assertCountEqual(
            round.get_hand(3), [44, 45, 46, 47, 52, 53, 54, 55, 60, 61, 62, 63, 70]
        )
        self.assertCountEqual(
            round.get_hand(0), [48, 49, 50, 51, 56, 57, 58, 59, 64, 65, 66, 67, 71]
        )

    def test_discard_pool(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=68))
        self.assertSequenceEqual(round.discard_tiles, [68])

    def test_discard_hand(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=68))
        self.assertCountEqual(
            round.get_hand(0), [4, 6, 8, 12, 16, 20, 24, 28, 32, 36, 84, 85, 86]
        )

    def test_draw(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=68))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        self.assertCountEqual(
            round.get_hand(1), [5, 9, 13, 17, 21, 25, 29, 33, 37, 38, 39, 87, 69, 7]
        )

    def test_chi_a(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(1, Action(action_type=ActionType.CHI_A))
        self.assertCountEqual(
            round.get_hand(1), [5, 9, 13, 17, 21, 33, 37, 38, 39, 87, 69]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[20, 25, 29])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSequenceEqual(round.discard_tiles, [9])

    def test_chi_b(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(1, Action(action_type=ActionType.CHI_B))
        self.assertCountEqual(
            round.get_hand(1), [5, 9, 13, 21, 29, 33, 37, 38, 39, 87, 69]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[17, 20, 25])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSequenceEqual(round.discard_tiles, [9])

    def test_chi_c(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=20))
        round.do_action(1, Action(action_type=ActionType.CHI_C))
        self.assertCountEqual(
            round.get_hand(1), [5, 9, 21, 25, 29, 33, 37, 38, 39, 87, 69]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.CHI, tiles=[13, 17, 20])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSequenceEqual(round.discard_tiles, [9])

    def test_pon(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
        round.do_action(1, Action(action_type=ActionType.PON))
        self.assertCountEqual(
            round.get_hand(1), [5, 9, 13, 17, 21, 25, 29, 33, 39, 87, 69]
        )
        self.assertCountEqual(
            round.get_calls(1), [Call(call_type=CallType.PON, tiles=[36, 37, 38])]
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSequenceEqual(round.discard_tiles, [9])

    def test_pon_change_turn(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=87))
        round.do_action(0, Action(action_type=ActionType.PON))
        self.assertCountEqual(
            round.get_hand(0), [8, 12, 16, 20, 24, 28, 32, 36, 86, 68, 6]
        )
        self.assertCountEqual(
            round.get_calls(0), [Call(call_type=CallType.PON, tiles=[87, 84, 85])]
        )
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=8))
        self.assertSequenceEqual(round.discard_tiles, [4, 8])

    def test_open_kan(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
        round.do_action(1, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(
            round.get_hand(1), [5, 9, 13, 17, 21, 25, 29, 33, 87, 69, 35]
        )
        self.assertCountEqual(
            round.get_calls(1),
            [Call(call_type=CallType.OPEN_KAN, tiles=[36, 37, 38, 39])],
        )
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSequenceEqual(round.discard_tiles, [9])

    def test_open_kan_change_turn(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=87))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        self.assertCountEqual(
            round.get_hand(0), [8, 12, 16, 20, 24, 28, 32, 36, 68, 6, 35]
        )
        self.assertCountEqual(
            round.get_calls(0),
            [Call(call_type=CallType.OPEN_KAN, tiles=[87, 84, 85, 86])],
        )
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=8))
        self.assertSequenceEqual(round.discard_tiles, [4, 8])

    def test_add_kan(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=87))
        round.do_action(0, Action(action_type=ActionType.PON))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=39))
        self.assertCountEqual(
            round.get_hand(1), [5, 7, 9, 13, 17, 21, 25, 29, 33, 69, 35]
        )
        self.assertCountEqual(
            round.get_calls(1),
            [Call(call_type=CallType.ADD_KAN, tiles=[39, 36, 37, 38])],
        )
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSequenceEqual(round.discard_tiles, [4, 9])

    def test_closed_kan(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.CLOSED_KAN, tile=44))
        self.assertCountEqual(
            round.get_hand(2), [10, 52, 53, 54, 55, 60, 61, 62, 63, 70, 35]
        )
        self.assertCountEqual(
            round.get_calls(2),
            [Call(call_type=CallType.CLOSED_KAN, tiles=[44, 45, 46, 47])],
        )
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.DISCARD, tile=52))
        self.assertSequenceEqual(round.discard_tiles, [4, 9, 52])

    def test_deck_2_start_hands(self):
        round = Round(tiles=test_deck2)
        self.assertCountEqual(
            round.get_hand(0), [4, 5, 6, 7, 16, 17, 18, 19, 28, 29, 30, 52, 37, 144]
        )
        self.assertCountEqual(round.get_calls(0), [])
        self.assertCountEqual(round.get_flowers(0), [164, 172])
        self.assertCountEqual(
            round.get_hand(1), [8, 9, 10, 11, 20, 21, 22, 23, 31, 53, 54, 55, 148]
        )
        self.assertCountEqual(round.get_calls(1), [])
        self.assertCountEqual(round.get_flowers(1), [168])
        self.assertCountEqual(
            round.get_hand(2), [44, 45, 46, 48, 49, 50, 124, 125, 128, 129, 130, 56, 60]
        )
        self.assertCountEqual(
            round.get_hand(3), [12, 13, 14, 15, 24, 25, 26, 27, 32, 33, 34, 35, 36]
        )

    def test_history(self):
        round = Round(tiles=test_deck1)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=36))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=87))
        round.do_action(0, Action(action_type=ActionType.PON))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=39))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=9))
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.DISCARD, tile=36)),
                (1, Action(action_type=ActionType.PON)),
                (1, Action(action_type=ActionType.DISCARD, tile=87)),
                (0, Action(action_type=ActionType.PON)),
                (0, Action(action_type=ActionType.DISCARD, tile=4)),
                (1, Action(action_type=ActionType.DRAW)),
                (1, Action(action_type=ActionType.ADD_KAN, tile=39)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.DISCARD, tile=9)),
            ],
        )

    def test_ron(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        round.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 0)
        self.assertCountEqual(
            win_info.hand, [44, 45, 46, 48, 49, 50, 124, 125, 128, 129, 130, 56, 60, 52]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_tsumo(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=8))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.TSUMO))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, None)
        self.assertCountEqual(
            win_info.hand, [44, 45, 46, 48, 49, 50, 124, 125, 128, 129, 130, 56, 60, 64]
        )
        self.assertCountEqual(win_info.calls, [])

    def test_chankan(self):
        round = Round(tiles=test_deck2)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        round.do_action(1, Action(action_type=ActionType.PON))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=31))
        round.do_action(0, Action(action_type=ActionType.OPEN_KAN))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.ADD_KAN, tile=55))
        round.do_action(2, Action(action_type=ActionType.RON))
        self.assertEqual(round.status, RoundStatus.END)
        win_info = round.win_info
        self.assertEqual(win_info.win_player, 2)
        self.assertEqual(win_info.lose_player, 1)
        self.assertCountEqual(
            win_info.hand, [44, 45, 46, 48, 49, 50, 124, 125, 128, 129, 130, 56, 60, 55]
        )
        self.assertCountEqual(win_info.calls, [])
        self.assertTrue(win_info.is_chankan)

    def test_auto_flower_history(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=True))
        self.assertSequenceEqual(
            round.history,
            [
                (0, Action(action_type=ActionType.FLOWER, tile=164)),
                (0, Action(action_type=ActionType.FLOWER, tile=172)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.FLOWER, tile=168)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.FLOWER, tile=176)),
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
                (1, Action(action_type=ActionType.FLOWER, tile=164)),
                (1, Action(action_type=ActionType.FLOWER, tile=172)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.FLOWER, tile=168)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.FLOWER, tile=176)),
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
                (0, Action(action_type=ActionType.FLOWER, tile=164)),
                (0, Action(action_type=ActionType.CONTINUE)),
                (1, Action(action_type=ActionType.CONTINUE)),
                (2, Action(action_type=ActionType.CONTINUE)),
                (3, Action(action_type=ActionType.CONTINUE)),
                (0, Action(action_type=ActionType.FLOWER, tile=168)),
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
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=164))
        self.assertCountEqual(round.get_flowers(0), [164])

    def test_start_flower_calls(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=164))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=172))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=176))
        self.assertCountEqual(round.get_flowers(0), [164, 172, 176])

    def test_start_flower_next_player(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=164))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=172))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=176))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=168))
        self.assertCountEqual(
            round.get_hand(1), [8, 9, 10, 11, 24, 25, 26, 27, 48, 49, 50, 51, 140]
        )
        self.assertCountEqual(round.get_flowers(1), [168])

    def test_start_flower_pass_all(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=164))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=172))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=176))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=168))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)

    def test_start_flower_loop_pass_all(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=164))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=172))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=168))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=176))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)

    def test_draw_flower(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=164))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=172))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=168))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.FLOWER, tile=176))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(2, Action(action_type=ActionType.CONTINUE))
        round.do_action(3, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.DISCARD, tile=8))
        round.do_action(2, Action(action_type=ActionType.DRAW))
        round.do_action(2, Action(action_type=ActionType.FLOWER, tile=180))
        self.assertCountEqual(round.get_flowers(2), [180])
        self.assertCountEqual(
            round.get_hand(2), [12, 13, 14, 15, 28, 29, 30, 31, 52, 53, 54, 55, 36, 184]
        )

    def test_priority(self):
        round = Round(tiles=test_deck4)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=4))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.CLOSED_KAN, tile=20))
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
        round.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=16))
        while round.wall_count > 14:
            actions = [action_set.default for action_set in round.allowed_actions]
            player, action = round.get_priority_action(actions)
            round.do_action(player, action)
        self.assertEqual(round.current_player, 0)
        self.assertEqual(round.status, RoundStatus.PLAY)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=52))
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
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=44))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.CLOSED_KAN, tile=4))
        round.do_action(1, Action(action_type=ActionType.CONTINUE))
        round.do_action(1, Action(action_type=ActionType.FLOWER, tile=192))
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
        round.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=64))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.TSUMO))
        self.assertFalse(round.win_info.is_tenhou)

    def test_chiihou(self):
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=44))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.TSUMO))
        self.assertTrue(round.win_info.is_chiihou)

    def test_not_chiihou_after_call(self):
        round = Round(tiles=test_deck_kan_tenhou)
        round.do_action(0, Action(action_type=ActionType.CLOSED_KAN, tile=64))
        round.do_action(0, Action(action_type=ActionType.CONTINUE))
        round.do_action(0, Action(action_type=ActionType.DISCARD, tile=44))
        round.do_action(1, Action(action_type=ActionType.DRAW))
        round.do_action(1, Action(action_type=ActionType.TSUMO))
        self.assertFalse(round.win_info.is_chiihou)
