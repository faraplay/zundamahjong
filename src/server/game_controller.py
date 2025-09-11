from flask_socketio import emit

from src.mahjong.action import Action, ActionType
from src.mahjong.game_options import GameOptions
from src.mahjong.round import RoundStatus
from src.mahjong.game import Game

from .player_info import Player


class GameController:
    def __init__(self, players: list[Player], options: GameOptions):
        self._players = players
        self._game = Game(options=options)
        self._submitted_actions = []
        self.set_default_submitted_actions()
        # self._game.round.display_info()

    def get_player_index(self, player: Player):
        try:
            return self._players.index(player)
        except ValueError:
            raise Exception(f"Player {player.id} not found in this game!")

    def _win_info(self):
        return (
            None
            if self._game.win is None
            else {
                "win": self._game.win.model_dump(),
                "scoring": self._game.scoring.model_dump(),
            }
        )

    def _round_info(self, index: int):
        hand = list(self._game.round.get_hand(index))
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
        if self._game.round.status == RoundStatus.END:
            actions = None
        else:
            actions = [
                action.model_dump()
                for action in self._game.round.allowed_actions(index).actions
            ]
        action_selected = self._submitted_actions[index] is not None
        return {
            "player": index,
            "wind_round": self._game.wind_round,
            "sub_round": self._game.sub_round,
            "draw_count": self._game.draw_count,
            "player_scores": self._game.player_scores,
            "tiles_left": self._game.round.tiles_left,
            "current_player": self._game.round.current_player,
            "status": self._game.round.status.value,
            "hand": hand,
            "history": history,
            "hand_counts": hand_counts,
            "discards": discards,
            "calls": calls,
            "flowers": flowers,
            "actions": actions,
            "action_selected": action_selected,
        }

    def _info(self, index: int):
        return {
            "player_count": self._game.player_count,
            "round_info": self._round_info(index),
            "win_info": self._win_info(),
        }

    def emit_info(self, player: Player):
        index = self.get_player_index(player)
        emit("info", self._info(index), to=player.id)

    def emit_info_all(self):
        for player_index, player in enumerate(self._players):
            emit("info", self._info(player_index), to=player.id)

    def set_default_submitted_actions(self):
        if self._game.round.status == RoundStatus.END:
            self._submitted_actions = [None] * self._game.player_count
        else:
            allowed_actions = [
                self._game.round.allowed_actions(player)
                for player in range(self._game.player_count)
            ]
            self._submitted_actions = [
                (
                    actions.default
                    if len(actions.actions) == 1
                    and (actions.default.action_type != ActionType.DISCARD)
                    else None
                )
                for actions in allowed_actions
            ]

    def _resolve_action(self):
        player, action = self._game.round.get_priority_action(self._submitted_actions)
        self._game.round.do_action(player, action)
        # self._game.round.display_info()

    def try_resolve_actions(self):
        action_resolve_count = 0
        while all(action is not None for action in self._submitted_actions):
            self._resolve_action()
            action_resolve_count += 1
            self.set_default_submitted_actions()
        if action_resolve_count > 0:
            self.emit_info_all()

    def submit_action(self, player: Player, action: Action):
        index = self.get_player_index(player)
        self._submitted_actions[index] = action
        # print(self._submitted_actions)
        self.try_resolve_actions()

    def start_next_round(self, player: Player):
        self.get_player_index(player)
        if not self._game.can_start_next_round:
            raise Exception("Cannot start next round!")
        print("Starting next round...")
        self._game.start_next_round()
        self.set_default_submitted_actions()
        # self._game.round.display_info()
        self.emit_info_all()
