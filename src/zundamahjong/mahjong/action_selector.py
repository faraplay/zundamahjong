from typing import final

from .action import Action
from .round import Round, RoundStatus


@final
class ActionSelector:
    def __init__(self, round: Round) -> None:
        self._round = round
        self._player_count = round.player_count
        self.reset_submitted_actions()
        self._resolve_actions()

    def submit_action(
        self, player_index: int, action: Action, history_index: int
    ) -> list[tuple[int, Action]] | None:
        if history_index != len(self._round.history):
            return None
        self._submitted_actions[player_index] = action
        return self._resolve_actions()

    def reset_submitted_actions(self) -> None:
        self._submitted_actions: list[Action | None] = [None] * self._player_count

    def _resolve_actions(self) -> list[tuple[int, Action]] | None:
        action_resolve_count = 0
        while self._round.status != RoundStatus.END:
            playeraction = self._round.get_priority_action(self._submitted_actions)
            if playeraction is None:
                break
            self._round.do_action(*playeraction)
            self.reset_submitted_actions()
            action_resolve_count += 1
        return self._round.history[len(self._round.history) - action_resolve_count :]
