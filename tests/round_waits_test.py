import unittest

from src.mahjong.form_hand import is_winning
from src.mahjong.tile import N, all_tiles
from src.mahjong.deck import Deck
from src.mahjong.hand import Hand
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
    def test_waits_wrong_hand_size(self) -> None:
        round = Round(tiles=test_deck1)
        self.assertSetEqual(round._hands[0].waits, frozenset())

    def test_waits(self) -> None:
        round = Round(tiles=test_deck2)
        self.assertSetEqual(round._hands[2].waits, frozenset({13, 16}))

    def test_8_tile_wait(self) -> None:
        hand = Hand(Deck(tiles=test_deck1))
        hand._tiles = [20, 21, 22, 30, 40, 50, 60, 61, 70, 71, 72, 73, 80]
        self.assertSetEqual(hand.waits, frozenset({1, 2, 3, 4, 5, 6, 8, 9}))


class RoundActionsWaitsCheckTest(unittest.TestCase):
    def check_waits(self, round: Round) -> None:
        for hand in round._hands:
            self.assertSetEqual(
                hand.waits,
                {
                    tile_value
                    for tile_value in all_tiles
                    if hand.tile_values.count(tile_value) < 4
                    and is_winning(hand._tiles + [tile_value * N])
                },
            )

    def test_draw(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=170))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)

    def test_chii(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=50))
        self.check_waits(round)
        round.do_action(
            1,
            OpenCallAction(action_type=ActionType.CHII, other_tiles=(61, 71)),
        )
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits(round)

    def test_pon(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.check_waits(round)
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits(round)

    def test_pon_change_turn(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        self.check_waits(round)
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        self.check_waits(round)

    def test_open_kan(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.check_waits(round)
        round.do_action(1, OpenKanAction(other_tiles=(91, 92, 93)))
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits(round)

    def test_open_kan_change_turn(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        self.check_waits(round)
        round.do_action(0, OpenKanAction(other_tiles=(210, 211, 212)))
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        self.check_waits(round)

    def test_add_kan(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=90))
        self.check_waits(round)
        round.do_action(
            1, OpenCallAction(action_type=ActionType.PON, other_tiles=(91, 92))
        )
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=213))
        self.check_waits(round)
        round.do_action(
            0, OpenCallAction(action_type=ActionType.PON, other_tiles=(210, 211))
        )
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)
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
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits(round)

    def test_closed_kan(self) -> None:
        round = Round(tiles=test_deck1)
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=21))
        self.check_waits(round)
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)
        round.do_action(2, ClosedKanAction(tiles=(110, 111, 112, 113)))
        self.check_waits(round)
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=130))
        self.check_waits(round)

    def test_draw_flower(self) -> None:
        round = Round(tiles=test_deck3, options=GameOptions(auto_replace_flowers=False))
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=410))
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=430))
        self.check_waits(round)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.FLOWER, tile=420))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.FLOWER, tile=440))
        self.check_waits(round)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(2, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(3, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(0, SimpleAction(action_type=ActionType.CONTINUE))
        self.check_waits(round)
        round.do_action(0, HandTileAction(action_type=ActionType.DISCARD, tile=10))
        self.check_waits(round)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=20))
        self.check_waits(round)
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        self.check_waits(round)
        round.do_action(2, HandTileAction(action_type=ActionType.FLOWER, tile=450))
        self.check_waits(round)
