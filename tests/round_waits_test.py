import unittest

from src.mahjong.round import Round
from src.mahjong.action import (
    ActionType,
    AddKanAction,
    ClosedKanAction,
    HandTileAction,
    OpenCallAction,
    OpenKanAction,
    SimpleAction,
)
from src.mahjong.call import (
    CallType,
    OpenCall,
)
from src.mahjong.game_options import GameOptions

from tests.decks import *


class RoundWaitsTest(unittest.TestCase):
    def test_waits_wrong_hand_size(self):
        round = Round(tiles=test_deck1)
        self.assertSetEqual(round._hands[0].waits, frozenset())

    def test_waits(self):
        round = Round(tiles=test_deck2)
        self.assertSetEqual(round._hands[2].waits, frozenset({13, 16}))

    def test_waits_dict(self):
        round = Round(tiles=test_deck1)
        self.assertDictEqual(
            round._hands[0].waits_dict,
            {
                10: frozenset({17}),
                12: frozenset({17}),
                20: frozenset(),
                30: frozenset(),
                40: frozenset(),
                50: frozenset(),
                60: frozenset(),
                70: frozenset(),
                80: frozenset(),
                90: frozenset(),
                170: frozenset({1, 4, 7}),
                210: frozenset(),
                211: frozenset(),
                212: frozenset(),
            },
        )

    def check_waits_dict_keys(self, round: Round):
        for hand in round._hands:
            self.assertSetEqual(set(hand.waits_dict.keys()), set(hand._tiles))

    def test_draw(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=170))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)

    def test_chii(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        self.check_waits_dict_keys(round)
        round.do_action(
            1,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(61, 71)),
        )
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits_dict_keys(round)

    def test_pon(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.check_waits_dict_keys(round)
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits_dict_keys(round)

    def test_pon_change_turn(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        self.check_waits_dict_keys(round)
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        self.check_waits_dict_keys(round)

    def test_open_kan(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.check_waits_dict_keys(round)
        round.do_action(1, OpenKanAction(other_tiles=(91, 92, 93)))
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits_dict_keys(round)

    def test_open_kan_change_turn(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        self.check_waits_dict_keys(round)
        round.do_action(0, OpenKanAction(other_tiles=(210, 211, 212)))
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        self.check_waits_dict_keys(round)

    def test_add_kan(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.check_waits_dict_keys(round)
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        self.check_waits_dict_keys(round)
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)
        round.do_action(
            1,
            AddKanAction(
                tile=93,
                pon_call=OpenCall(
                    call_type=CallType.PON,
                    called_player_index=0,
                    called_tile=90,
                    other_tiles=(91, 92),
                ),
            ),
        )
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits_dict_keys(round)

    def test_closed_kan(self):
        round = Round(tiles=test_deck1)
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits_dict_keys(round)
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)
        round.do_action(2, ClosedKanAction(tiles=(110, 111, 112, 113)))
        self.check_waits_dict_keys(round)
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        self.check_waits_dict_keys(round)

    def test_draw_flower(self):
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        self.check_waits_dict_keys(round)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=420))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        self.check_waits_dict_keys(round)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits_dict_keys(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits_dict_keys(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        self.check_waits_dict_keys(round)
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits_dict_keys(round)
        round.do_action(2, HandTileAction(action_type=ActionType.FLOWER, tile=450))
        self.check_waits_dict_keys(round)
