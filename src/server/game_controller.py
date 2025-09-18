from threading import Lock
from src.mahjong.action import Action
from src.mahjong.game_options import GameOptions
from src.mahjong.round import RoundStatus
from src.mahjong.game import Game

from .sio import sio
from .player_info import Player


class GameController:
    def __init__(self, players: list[Player], options: GameOptions):
        self._players = players
        self._game = Game(options=options)
        self._lock = Lock()

    def emit_info(self, player: Player):
        with self._lock:
            index = self._get_player_index(player)
            sio.emit("info", self._info(index), to=player.id)

    def emit_info_all(self):
        with self._lock:
            self._emit_info_all_inner()

    def submit_action(self, player: Player, action: Action, history_index: int):
        with self._lock:
            player_index = self._get_player_index(player)
            performed_actions = self._game.submit_action(
                player_index, action, history_index
            )
            if performed_actions is not None and len(performed_actions) > 0:
                self._emit_info_all_inner()

    def start_next_round(self, player: Player):
        with self._lock:
            self._get_player_index(player)
            if not self._game.can_start_next_round:
                raise Exception("Cannot start next round!")
            self._game.start_next_round()
            self._emit_info_all_inner()

    def _get_player_index(self, player: Player):
        try:
            return self._players.index(player)
        except ValueError:
            raise Exception(f"Player {player.id} not found in this game!")

    def _game_info(self):
        return {
            "player_names": [player.name for player in self._players],
            "wind_round": self._game.wind_round,
            "sub_round": self._game.sub_round,
            "draw_count": self._game.draw_count,
            "player_scores": self._game.player_scores,
        }

    def _round_info(self):
        history = [
            {"player": action[0], "action": action[1].model_dump()}
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

    def _player_info(self, index: int):
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

    def _info(self, index: int):
        return {
            "player_count": self._game.player_count,
            "player_index": index,
            "is_game_end": self._game.is_game_end,
            "game_info": self._game_info(),
            "round_info": self._round_info(),
            "player_info": self._player_info(index),
            "win_info": self._game.win.model_dump() if self._game.win else None,
            "scoring_info": (
                self._game.scoring.model_dump() if self._game.scoring else None
            ),
        }

    def _emit_info_all_inner(self):
        for index, player in enumerate(self._players):
            sio.emit("info", self._info(index), to=player.id)
