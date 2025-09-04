from .exceptions import InvalidOperationException
from .tile import Tile
from .game_options import GameOptions
from .round import Round, RoundStatus
from .scoring import ScoringHand


class Game:
    def __init__(
        self,
        first_deck_tiles: list[Tile] | None = None,
        options: GameOptions = GameOptions(),
    ):
        self._player_count = options.player_count
        self._options = options
        self._wind_round: int = 0
        self._sub_round: int = 0
        self._player_seats = tuple(range(self._player_count))
        self._player_scores = [options.start_score] * self._player_count
        self._draw_count: int = 0
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
    def draw_count(self):
        return self._draw_count

    @property
    def player_scores(self):
        return tuple(self._player_scores)

    @property
    def win_scoring(self):
        return self._win_scoring

    @property
    def is_end(self):
        if self._round.status != RoundStatus.END:
            return False
        return (
            self._next_round() >= self._options.game_length
            and not self.is_dealer_repeat()
        )

    def get_seat(self, player: int):
        return (player + self._sub_round) % self._player_count

    def get_player(self, seat: int):
        return (seat - self._sub_round) % self._player_count

    def start_next_round(self, deck_tiles: list[int] | None = None):
        if self._round.status != RoundStatus.END:
            raise InvalidOperationException()
        if self.is_end:
            raise InvalidOperationException()
        if not self.is_dealer_repeat():
            self._wind_round, self._sub_round = self._next_round()
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

    def _next_round(self):
        next_wind_round = self._wind_round
        next_sub_round = self._sub_round + 1
        if next_sub_round >= self._player_count:
            next_wind_round += 1
            next_sub_round = 0
        return next_wind_round, next_sub_round

    def _create_round(self, deck_tiles: list[Tile] | None):
        def on_round_end():
            self._calculate_win_score()

        self._round = Round(
            wind_round=self._wind_round % 4,
            tiles=deck_tiles,
            options=self._options,
            round_end_callback=on_round_end,
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
