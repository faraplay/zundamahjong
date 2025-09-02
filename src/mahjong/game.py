from .tile import Tile
from .game_options import GameOptions
from .round import Round
from .scoring import ScoringHand


class Game:
    def __init__(
        self,
        first_deck_tiles: list[Tile] | None = None,
        options: GameOptions = GameOptions(),
    ):
        self._player_count = options.player_count
        self._options = options
        self._wind_round = 0
        self._sub_round = 0
        self._player_seats = tuple(range(self._player_count))
        self._player_scores = [options.start_score] * self._player_count
        self._draw_count = 0
        self._create_round(first_deck_tiles)

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
    def player_scores(self):
        return tuple(self._player_scores)

    @property
    def win_scoring(self):
        return self._win_scoring

    def get_seat(self, player: int):
        return (player + self._sub_round) % self._player_count

    def get_player(self, seat: int):
        return (seat - self._sub_round) % self._player_count

    def start_next_round(self, deck_tiles: list[int] | None = None):
        if self.is_dealer_repeat():
            self._sub_round += 1
            if self._sub_round >= self._player_count:
                self._wind_round += 1
                self._sub_round = 0
        self._player_seats = tuple(
            (player + self._sub_round) % self._player_count
            for player in range(self._player_count)
        )
        if self._win_scoring is None:
            self._draw_count += 1
        else:
            self._draw_count = 0
        self._create_round(deck_tiles)

    def is_dealer_repeat(self):
        if self._win_scoring is None:
            return True
        else:
            return self._win_scoring.win.win_seat == 0

    def _create_round(self, deck_tiles: list[Tile] | None):
        def self_calculate_win_score():
            self._calculate_win_score()

        self._round = Round(
            tiles=deck_tiles,
            options=self._options,
            round_end_callback=self_calculate_win_score,
        )
        self._win_scoring = None

    def _calculate_win_score(self):
        if self._round.win_info is None:
            self._win_scoring = None
        else:
            win_scoring = ScoringHand(
                self._round.win_info, self._options
            ).get_win_scoring()
            self._win_scoring = win_scoring
            for player in range(self._player_count):
                self._player_scores[player] += win_scoring.scoring.seat_scores[
                    self.get_seat(player)
                ]
