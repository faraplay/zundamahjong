from typing import final

from .action import Action
from .round import Round, RoundStatus


@final
class ActionSelector:
    """
    Helps to select the highest-priority action out of each player's
    submitted actions.

    This object controls a :py:class:`Round` object representing a round
    of mahjong. When playing the round, each player can submit an action to
    this :py:class:`ActionSelector` object. This object will then select
    the legal action with highest priority and perform that action
    on the :py:class:`Round` object.

    :param round: The :py:class:`Round` object that this object will control.
    """

    def __init__(self, round: Round) -> None:
        self._round = round
        self._player_count = round.player_count
        self._reset_submitted_actions()
        self._resolve_actions()

    def submit_action(
        self, player_index: int, action: Action, history_index: int
    ) -> list[tuple[int, Action]] | None:
        """
        Submit an action for a player at a given moment (specified by
        the :py:data:`history_index` argument) in the round.

        If the :py:data:`history_index` argument does not match the
        current total number of actions performed in the round,
        this will do nothing. Otherwise, the specified action is submitted
        for the specified player.

        This will trigger an action in the associated :py:class:`Round` object
        if enough actions have been submitted to determine what the highest
        priority action will be, e.g. if the submitted action is
        the highest possible priority action, or if all players have submitted
        actions.

        If an action is triggered, then all submissions are reset, leaving
        players free to submit their next actions.

        :param player_index: The index of the player submitting an action.
        :param action: The action to submit.
        :param history_index: The total number of actions performed so far
                              in the game when the player submitted the action.
        :return: A list of tuples containing the player index and the
                 :py:class:`Action` of each action performed in the round
                 after this action was submitted, or ``None`` if the
                 :py:data:`history_index` argument does not match.
        """
        if history_index != len(self._round.history):
            return None
        self._submitted_actions[player_index] = action
        return self._resolve_actions()

    def _reset_submitted_actions(self) -> None:
        self._submitted_actions: list[Action | None] = [None] * self._player_count

    def _resolve_actions(self) -> list[tuple[int, Action]]:
        action_resolve_count = 0
        while self._round.status != RoundStatus.END:
            playeraction = self._round.get_priority_action(self._submitted_actions)
            if playeraction is None:
                break
            self._round.do_action(*playeraction)
            self._reset_submitted_actions()
            action_resolve_count += 1
        return self._round.history[len(self._round.history) - action_resolve_count :]
