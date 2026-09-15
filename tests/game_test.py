import pytest

from tests.decks import test_deck2, test_deck4, test_deck6, test_deck_riichi
from zundamahjong.mahjong.action import (
    ActionType,
    ClosedKanAction,
    HandTileAction,
    SimpleAction,
)
from zundamahjong.mahjong.exceptions import InvalidOperationException
from zundamahjong.mahjong.game import Game
from zundamahjong.mahjong.game_options import GameOptions
from zundamahjong.mahjong.round import RoundStatus


class TestGame:
    def test_first_round(self) -> None:
        game = Game(first_deck_tiles=test_deck2)
        assert game.wind_round == 0
        assert game.sub_round == 0
        assert game.player_scores == (0.0, 0.0, 0.0, 0.0)

    def test_no_win_during_first_round(self) -> None:
        game = Game(first_deck_tiles=test_deck2)
        assert game.win is None

    def test_cannot_start_next_round_during_round(self) -> None:
        game = Game(first_deck_tiles=test_deck2)
        with pytest.raises(InvalidOperationException):
            game.start_next_round(test_deck2)

    def test_auto_calculate_score(self) -> None:
        game = Game(first_deck_tiles=test_deck2)
        game.round.do_action(
            0, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(2, SimpleAction(action_type=ActionType.RON))
        assert game.scoring is not None
        assert list(game.player_scores) == game.scoring.player_scores

    def test_dealer_repeat_next_round(self) -> None:
        game = Game(first_deck_tiles=test_deck6)
        game.round.do_action(0, SimpleAction(action_type=ActionType.TSUMO))
        game.start_next_round(test_deck2)
        assert game.wind_round == 0
        assert game.sub_round == 0

    def test_dealer_nonrepeat_next_round(self) -> None:
        game = Game(first_deck_tiles=test_deck2)
        game.round.do_action(
            0, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(2, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        assert game.wind_round == 0
        assert game.sub_round == 1

    def test_next_wind_round(self) -> None:
        game = Game(
            first_deck_tiles=test_deck2,
            options=GameOptions(game_length_wind_rounds=2, game_length_sub_rounds=0),
        )
        game.round.do_action(
            0, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(2, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(
            1, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(3, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(
            2, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(0, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(
            3, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(1, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        assert game.wind_round == 1
        assert game.sub_round == 0
        assert game.round.wind_round == 1

    def test_one_round_game(self) -> None:
        game = Game(
            first_deck_tiles=test_deck2,
            options=GameOptions(game_length_wind_rounds=0, game_length_sub_rounds=1),
        )
        game.round.do_action(
            0, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(2, SimpleAction(action_type=ActionType.RON))
        assert game.is_game_end

    def test_cannot_start_next_round_at_end(self) -> None:
        game = Game(
            first_deck_tiles=test_deck2,
            options=GameOptions(game_length_wind_rounds=0, game_length_sub_rounds=1),
        )
        game.round.do_action(
            0, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(2, SimpleAction(action_type=ActionType.RON))
        with pytest.raises(InvalidOperationException):
            game.start_next_round()

    def test_last_round_dealer_repeat(self) -> None:
        game = Game(
            first_deck_tiles=test_deck2,
            options=GameOptions(game_length_wind_rounds=1, game_length_sub_rounds=0),
        )
        game.round.do_action(
            0, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(2, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(
            1, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(3, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck2)
        game.round.do_action(
            2, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(0, SimpleAction(action_type=ActionType.RON))
        game.start_next_round(test_deck6)
        game.round.do_action(3, SimpleAction(action_type=ActionType.TSUMO))
        assert not game.is_game_end
        game.start_next_round(test_deck2)
        game.round.do_action(
            3, HandTileAction(action_type=ActionType.DISCARD, tile=130)
        )
        game.round.do_action(1, SimpleAction(action_type=ActionType.RON))
        assert game.is_game_end

    def test_draw_count(self) -> None:
        game = Game(first_deck_tiles=test_deck4)
        assert game.draw_count == 0
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            playeraction = round.get_priority_action(actions)
            assert playeraction is not None
            round.do_action(*playeraction)
        assert game.draw_count == 0

        game.start_next_round(test_deck4)
        assert game.draw_count == 1
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            playeraction = round.get_priority_action(actions)
            assert playeraction is not None
            round.do_action(*playeraction)
        assert game.draw_count == 1

        game.start_next_round(test_deck6)
        assert game.draw_count == 2
        game.round.do_action(0, SimpleAction(action_type=ActionType.TSUMO))
        assert game.draw_count == 2

        game.start_next_round(test_deck2)
        assert game.draw_count == 0

    def test_win_draw_count(self) -> None:
        game = Game(first_deck_tiles=test_deck4)
        assert game.draw_count == 0
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            playeraction = round.get_priority_action(actions)
            assert playeraction is not None
            round.do_action(*playeraction)
        assert game.draw_count == 0

        game.start_next_round(test_deck4)
        assert game.draw_count == 1
        round = game.round
        while round.status != RoundStatus.END:
            actions = [action_set.default for action_set in round.allowed_actions]
            playeraction = round.get_priority_action(actions)
            assert playeraction is not None
            round.do_action(*playeraction)
        assert game.draw_count == 1

        game.start_next_round(test_deck6)
        assert game.draw_count == 2
        game.round.do_action(0, SimpleAction(action_type=ActionType.TSUMO))
        assert game.win is not None
        assert game.win.draw_count == 2

    def test_riichi_cost(self) -> None:
        game = Game(
            options=GameOptions(
                start_score=500.0, riichi_cost=100.0, can_riichi_negative_score=False
            ),
            first_deck_tiles=test_deck_riichi,
        )
        round = game.round
        assert game.player_scores == (500.0, 500.0, 500.0, 500.0)
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=160))
        assert game.player_scores == (400.0, 500.0, 500.0, 500.0)

    def test_riichi_win_takes_pot(self) -> None:
        game = Game(
            options=GameOptions(
                start_score=500.0, riichi_cost=100.0, can_riichi_negative_score=False
            ),
            first_deck_tiles=test_deck_riichi,
        )
        round = game.round
        assert game.player_scores == (500.0, 500.0, 500.0, 500.0)
        round.do_action(0, HandTileAction(action_type=ActionType.RIICHI, tile=160))
        assert game.player_scores == (400.0, 500.0, 500.0, 500.0)
        round.do_action(1, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(1, HandTileAction(action_type=ActionType.DISCARD, tile=350))
        round.do_action(2, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(2, HandTileAction(action_type=ActionType.DISCARD, tile=13))
        round.do_action(3, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(3, HandTileAction(action_type=ActionType.DISCARD, tile=223))
        round.do_action(0, SimpleAction(action_type=ActionType.DRAW))
        round.do_action(0, SimpleAction(action_type=ActionType.TSUMO))
        assert game.player_scores == (38900.0, -12300.0, -12300.0, -12300.0)

    def test_too_poor_for_riichi(self) -> None:
        game = Game(
            options=GameOptions(
                start_score=50.0, riichi_cost=100.0, can_riichi_negative_score=False
            ),
            first_deck_tiles=test_deck_riichi,
        )
        assert game.player_scores == (50.0, 50.0, 50.0, 50.0)
        assert game.round.allowed_actions[0].actions == [
            HandTileAction(action_type=ActionType.DISCARD, tile=230),
            HandTileAction(action_type=ActionType.DISCARD, tile=10),
            HandTileAction(action_type=ActionType.DISCARD, tile=11),
            HandTileAction(action_type=ActionType.DISCARD, tile=12),
            HandTileAction(action_type=ActionType.DISCARD, tile=130),
            HandTileAction(action_type=ActionType.DISCARD, tile=140),
            HandTileAction(action_type=ActionType.DISCARD, tile=150),
            HandTileAction(action_type=ActionType.DISCARD, tile=151),
            HandTileAction(action_type=ActionType.DISCARD, tile=152),
            HandTileAction(action_type=ActionType.DISCARD, tile=153),
            HandTileAction(action_type=ActionType.DISCARD, tile=160),
            HandTileAction(action_type=ActionType.DISCARD, tile=220),
            HandTileAction(action_type=ActionType.DISCARD, tile=221),
            HandTileAction(action_type=ActionType.DISCARD, tile=222),
            ClosedKanAction(tiles=(150, 151, 152, 153)),
        ]

    def test_can_riichi_into_negative_score(self) -> None:
        game = Game(
            options=GameOptions(
                start_score=50.0, riichi_cost=100.0, can_riichi_negative_score=True
            ),
            first_deck_tiles=test_deck_riichi,
        )
        assert game.player_scores == (50.0, 50.0, 50.0, 50.0)
        assert game.round.allowed_actions[0].actions == [
            HandTileAction(action_type=ActionType.DISCARD, tile=230),
            HandTileAction(action_type=ActionType.DISCARD, tile=10),
            HandTileAction(action_type=ActionType.DISCARD, tile=11),
            HandTileAction(action_type=ActionType.DISCARD, tile=12),
            HandTileAction(action_type=ActionType.DISCARD, tile=130),
            HandTileAction(action_type=ActionType.DISCARD, tile=140),
            HandTileAction(action_type=ActionType.DISCARD, tile=150),
            HandTileAction(action_type=ActionType.DISCARD, tile=151),
            HandTileAction(action_type=ActionType.DISCARD, tile=152),
            HandTileAction(action_type=ActionType.DISCARD, tile=153),
            HandTileAction(action_type=ActionType.DISCARD, tile=160),
            HandTileAction(action_type=ActionType.DISCARD, tile=220),
            HandTileAction(action_type=ActionType.DISCARD, tile=221),
            HandTileAction(action_type=ActionType.DISCARD, tile=222),
            HandTileAction(action_type=ActionType.RIICHI, tile=130),
            HandTileAction(action_type=ActionType.RIICHI, tile=160),
            HandTileAction(action_type=ActionType.RIICHI, tile=230),
            ClosedKanAction(tiles=(150, 151, 152, 153)),
        ]
