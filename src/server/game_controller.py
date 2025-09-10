from flask_socketio import emit

from src.mahjong.action import Action, ActionType
from src.mahjong.game_options import GameOptions
from src.mahjong.round import RoundStatus
from src.mahjong.game import Game

from .player_info import PlayerInfo


class GameController:
    def __init__(self, player_ids: list[str], options: GameOptions):
        self._player_ids = player_ids
        self._game = Game(options=options)
        self._submitted_actions = []
        self.set_default_submitted_actions()
        # self._game.round.display_info()

    def validate_player_id(self, player_info):
        if self._player_ids[player_info.player] != player_info.player_id:
            raise Exception(
                f"Player id {player_info.player_id} and game player id "
                + f"{self._player_ids[player_info.player]} do not match!"
            )

    def _win_info(self):
        return (
            None
            if self._game.win is None
            else {
                "win": self._game.win.model_dump(),
                "scoring": self._game.scoring.model_dump(),
            }
        )

    def _round_info(self, player: int):
        hand = list(self._game.round.get_hand(player))
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
                for action in self._game.round.allowed_actions(player).actions
            ]
        action_selected = self._submitted_actions[player] is not None
        return {
            "player": player,
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

    def _game_info(self, player: int):
        return {
            "player_count": self._game.player_count,
            "round_info": self._round_info(player),
            "win_info": self._win_info(),
        }

    def emit_info(self, player_info: PlayerInfo):
        self.validate_player_id(player_info)
        emit("info", self._game_info(player_info.player), to=player_info.player_id)

    def emit_info_all(self):
        for player, player_id in enumerate(self._player_ids):
            emit("info", self._game_info(player), to=player_id)

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

    def submit_action(self, player_info: PlayerInfo, action: Action):
        self.validate_player_id(player_info)
        self._submitted_actions[player_info.player] = action
        # print(self._submitted_actions)
        self.try_resolve_actions()

    def start_next_round(self, player_info: PlayerInfo):
        self.validate_player_id(player_info)
        if not self._game.can_start_next_round:
            raise Exception("Cannot start next round!")
        print("Starting next round...")
        self._game.start_next_round()
        self.set_default_submitted_actions()
        # self._game.round.display_info()
        self.emit_info_all()
