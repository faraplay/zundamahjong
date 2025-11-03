import uuid
from typing import final

from .action import Action
from .action_selector import ActionSelector
from .exceptions import InvalidOperationException
from .game_options import GameOptions
from .round import Round, RoundStatus
from .scoring import Scorer, Scoring
from .tile import TileId
from .win import Win


@final
class Game:
    """
    Represents a game of mahjong, which consists of multiple rounds of mahjong.

    :param first_deck_tiles: (Optional) A list of tiles to use as the deck
                             in the first round.
    :param options: (Optional) A :py:class:`GameOptions` object with the game
                    options to use. If this is ``None`` the default options are used.
    """

    def __init__(
        self,
        *,
        first_deck_tiles: list[TileId] | None = None,
        options: GameOptions | None = None,
    ):
        if options is not None:
            _options = options
        else:
            _options = GameOptions()
        self._uuid = uuid.uuid4()
        self._player_count = _options.player_count
        self._options = _options
        self._wind_round: int = 0
        self._sub_round: int = 0
        self._player_scores = [_options.start_score] * self._player_count
        self._win: Win | None = None
        self._scoring: Scoring | None = None
        self._draw_count: int = 0
        self._create_round(first_deck_tiles)

    @property
    def uuid(self) -> uuid.UUID:
        return self._uuid

    @property
    def player_count(self) -> int:
        "The number of players."
        return self._player_count

    @property
    def wind_round(self) -> int:
        "The current wind round."
        return self._wind_round

    @property
    def sub_round(self) -> int:
        "The current sub-round number of the current round."
        return self._sub_round

    @property
    def round(self) -> Round:
        "The :py:class:`Round` object representing the current round."
        return self._round

    @property
    def draw_count(self) -> int:
        "The number of consecutive draws before the current round."
        return self._draw_count

    @property
    def player_scores(self) -> tuple[float, ...]:
        "A tuple containing the players' current scores."
        return tuple(self._player_scores)

    @property
    def win(self) -> Win | None:
        """
        A :py:class:`Win` object representing the win of the current round,
        or ``None`` if no player has won yet.
        """
        return self._win

    @property
    def scoring(self) -> Scoring | None:
        """
        A :py:class:`Scoring` object representing the score data of the
        current round, or ``None`` if no player has won yet.
        """
        return self._scoring

    @property
    def can_start_next_round(self) -> bool:
        """
        Whether the next round can be started.

        The next round can be started if the current round has ended
        and it is not the last round.
        """
        return self._round.status == RoundStatus.END and not self.is_game_end

    @property
    def is_dealer_repeat(self) -> bool:
        """
        Whether the next round will repeat the sub-round number.

        The next round will repeat the sub-round number if nobody has
        won (it is a draw) or if the winner is the dealer.
        """
        if self._win is None:
            return True
        else:
            return self._win.win_player == self.sub_round

    @property
    def is_game_end(self) -> bool:
        """
        Whether the game has ended.

        The game has ended if the round has ended and it is the last
        round, which holds if the number of the next round would exceed
        the total game length.
        """
        return (
            self._round.status == RoundStatus.END
            and self._next_round() >= self._options.game_length
        )

    def submit_action(
        self, player_index: int, action: Action, history_index: int
    ) -> list[tuple[int, Action]] | None:
        """
        Submit an action for a player at a given moment (specified by
        the :py:data:`history_index` argument) in the round.

        See :obj:`.action_selector.ActionSelector.submit_action`
        for more information.

        :param player_index: The index of the player submitting an action.
        :param action: The action to submit.
        :param history_index: The total number of actions performed so far
                              in the game when the player submitted the action.
        :return: A list of tuples containing the player index and the
                 :py:class:`Action` of each action performed in the round
                 after this action was submitted, or ``None`` if the
                 :py:data:`history_index` argument does not match.
        """
        return self._action_selector.submit_action(player_index, action, history_index)

    def start_next_round(self, deck_tiles: list[int] | None = None) -> None:
        """
        Start the next round.

        This will throw an :py:class:`InvalidOperationException` if
        the current round has not ended or if this is the last round.

        :param deck_tiles: (Optional) A list of tiles to use as the deck in the
                           next round.
        """
        if not self.can_start_next_round:
            raise InvalidOperationException()
        self._wind_round, self._sub_round = self._next_round()
        if self._win is None:
            self._draw_count += 1
        else:
            self._draw_count = 0
        self._create_round(deck_tiles)

    def _next_round(self) -> tuple[int, int]:
        if self.is_dealer_repeat:
            return self._wind_round, self._sub_round
        next_wind_round = self._wind_round
        next_sub_round = self._sub_round + 1
        if next_sub_round >= self._player_count:
            next_wind_round += 1
            next_sub_round = 0
        return next_wind_round, next_sub_round

    def _create_round(self, deck_tiles: list[TileId] | None) -> None:
        def on_round_end() -> None:
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

    def _calculate_win_score(self) -> None:
        self._win = self._round.win
        if self._win is None:
            self._scoring = None
        else:
            scoring = Scorer.score(self._win, self._options)
            self._scoring = scoring
            for player in range(self._player_count):
                self._player_scores[player] += scoring.player_scores[player]
