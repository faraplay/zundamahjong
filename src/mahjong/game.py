from typing import Optional

from .exceptions import InvalidOperationException
from .tile import TileId
from .action import Action
from .game_options import GameOptions
from .win import Win
from .round import Round, RoundStatus
from .scoring import Scoring, Scorer
from .action_selector import ActionSelector


class Game:
    def __init__(
        self,
        *,
        first_deck_tiles: Optional[list[TileId]] = None,
        options: GameOptions = GameOptions(),
    ):
        self._player_count = options.player_count
        self._options = options
        self._wind_round: int = 0
        self._sub_round: int = 0
        self._player_scores = [options.start_score] * self._player_count
        self._win: Optional[Win] = None
        self._scoring: Optional[Scoring] = None
        self._draw_count: int = 0
        self._create_round(first_deck_tiles)

    @property
    def player_count(self):
        return self._player_count

    @property
    def wind_round(self):
        return self._wind_round

    @property
    def sub_round(self):
        return self._sub_round

    @property
    def round(self):
        return self._round

    @property
    def draw_count(self):
        return self._draw_count

    @property
    def player_scores(self):
        return tuple(self._player_scores)

    @property
    def win(self):
        return self._win

    @property
    def scoring(self):
        return self._scoring

    @property
    def can_start_next_round(self):
        return self._round.status == RoundStatus.END and not self.is_game_end

    @property
    def is_dealer_repeat(self):
        if self._win is None:
            return True
        else:
            return self._win.win_player == self.sub_round

    @property
    def is_game_end(self):
        if self._round.status != RoundStatus.END:
            return False
        return (
            self._next_round() >= self._options.game_length
            and not self.is_dealer_repeat
        )

    def submit_action(self, player_index: int, action: Action, history_index: int):
        return self._action_selector.submit_action(player_index, action, history_index)

    def start_next_round(self, deck_tiles: Optional[list[int]] = None):
        if not self.can_start_next_round:
            raise InvalidOperationException()
        if not self.is_dealer_repeat:
            self._wind_round, self._sub_round = self._next_round()
        if self._win is None:
            self._draw_count += 1
        else:
            self._draw_count = 0
        self._create_round(deck_tiles)

    def _next_round(self):
        next_wind_round = self._wind_round
        next_sub_round = self._sub_round + 1
        if next_sub_round >= self._player_count:
            next_wind_round += 1
            next_sub_round = 0
        return next_wind_round, next_sub_round

    def _create_round(self, deck_tiles: Optional[list[TileId]]):
        def on_round_end():
            self._calculate_win_score()

        self._round = Round(
            wind_round=self._wind_round % 4,
            sub_round=self._sub_round,
            draw_count=self._draw_count,
            tiles=deck_tiles,
            options=self._options,
            round_end_callback=on_round_end,
        )
        self._win = None
        self._scoring = None
        self._action_selector = ActionSelector(self._round)

    def _calculate_win_score(self):
        self._win = self._round.win_info
        if self._win is None:
            self._scoring = None
        else:
            scoring = Scorer.score(self._round.win_info, self._options)
            self._scoring = scoring
            for player in range(self._player_count):
                self._player_scores[player] += scoring.player_scores[player]
