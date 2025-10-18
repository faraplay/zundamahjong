from threading import Lock
from typing import Any, final
from random import sample

from ..mahjong.action import Action
from ..mahjong.game_options import GameOptions
from ..mahjong.round import RoundStatus
from ..mahjong.game import Game

from .sio import sio
from ..types.player import Player


@final
class GameController:
    def __init__(self, players: list[Player], options: GameOptions) -> None:
        self._players = sample(players, len(players))
        self._game = Game(options=options)
        self._lock = Lock()
        with self._lock:
            self._emit_info_all_inner(self._game.round.history)

    def emit_info(self, player: Player) -> None:
        with self._lock:
            index = self._get_player_index(player)
            sio.emit("info", self._info(index, []), to=player.id)

    def submit_action(self, player: Player, action: Action, history_index: int) -> None:
        with self._lock:
            player_index = self._get_player_index(player)
            history_updates = self._game.submit_action(
                player_index, action, history_index
            )
            if history_updates is not None and len(history_updates) > 0:
                self._emit_info_all_inner(history_updates)

    def start_next_round(self, player: Player) -> None:
        with self._lock:
            self._get_player_index(player)
            if not self._game.can_start_next_round:
                raise Exception("Cannot start next round!")
            self._game.start_next_round()
            self._emit_info_all_inner(self._game.round.history)

    def _get_player_index(self, player: Player) -> int:
        try:
            return self._players.index(player)
        except ValueError:
            raise Exception(f"Player {player.id} not found in this game!")

    def _game_info(self) -> dict[str, Any]:
        return {
            "players": [player.model_dump() for player in self._players],
            "wind_round": self._game.wind_round,
            "sub_round": self._game.sub_round,
            "draw_count": self._game.draw_count,
            "player_scores": self._game.player_scores,
        }

    def _round_info(self) -> dict[str, Any]:
        history = [
            {"player_index": action[0], "action": action[1].model_dump()}
            for action in self._game.round.history
        ]
        hand_counts = [
            len(self._game.round.get_hand(player))
            for player in range(self._game.player_count)
        ]
        discards = [discard.model_dump() for discard in self._game.round.discards]
        calls = [
            [call.model_dump() for call in self._game.round.get_calls(player)]
            for player in range(self._game.player_count)
        ]
        flowers = [
            self._game.round.get_flowers(player)
            for player in range(self._game.player_count)
        ]
        return {
            "tiles_left": self._game.round.tiles_left,
            "current_player": self._game.round.current_player,
            "status": self._game.round.status.value,
            "hand_counts": hand_counts,
            "discards": discards,
            "calls": calls,
            "flowers": flowers,
            "history": history,
        }

    def _player_info(self, index: int) -> dict[str, Any]:
        hand = list(self._game.round.get_hand(index))
        if self._game.round.status == RoundStatus.END:
            actions = []
        else:
            actions = [
                action.model_dump()
                for action in self._game.round.allowed_actions[index].actions
            ]
        action_selected = False
        return {
            "hand": hand,
            "last_tile": self._game.round.last_tile,
            "actions": actions,
            "action_selected": action_selected,
        }

    def _info(
        self, index: int, history_updates: list[tuple[int, Action]]
    ) -> dict[str, Any]:
        return {
            "player_count": self._game.player_count,
            "player_index": index,
            "is_game_end": self._game.is_game_end,
            "game_info": self._game_info(),
            "round_info": self._round_info(),
            "history_updates": [
                {
                    "player_index": history_item[0],
                    "action": history_item[1].model_dump(),
                }
                for history_item in history_updates
            ],
            "player_info": self._player_info(index),
            "win_info": self._game.win.model_dump() if self._game.win else None,
            "scoring_info": (
                self._game.scoring.model_dump() if self._game.scoring else None
            ),
        }

    def _emit_info_all_inner(self, history_updates: list[tuple[int, Action]]) -> None:
        for index, player in enumerate(self._players):
            sio.emit("info", self._info(index, history_updates), to=player.id)
