from collections.abc import Sequence
from random import sample
from threading import Lock
from typing import Optional, final

from pydantic import BaseModel

from ..mahjong.action import Action
from ..mahjong.call import Call
from ..mahjong.discard_pool import Discard
from ..mahjong.game import Game
from ..mahjong.game_options import GameOptions
from ..mahjong.round import RoundStatus
from ..mahjong.scoring import Scoring
from ..mahjong.tile import TileId
from ..mahjong.win import Win
from ..types.player import Player
from .sio import sio


class GameInfo(BaseModel):
    players: list[Player]
    wind_round: int
    sub_round: int
    draw_count: int
    player_scores: tuple[float, ...]


class HistoryItem(BaseModel):
    player_index: int
    action: Action


class RoundInfo(BaseModel):
    tiles_left: int
    current_player: int
    status: RoundStatus
    hand_counts: list[int]
    discards: list[Discard]
    calls: list[Sequence[Call]]
    flowers: list[Sequence[TileId]]
    history: list[HistoryItem]


class PlayerInfo(BaseModel):
    hand: list[TileId]
    last_tile: TileId
    actions: list[Action]
    action_selected: bool


class AllInfo(BaseModel):
    player_count: int
    player_index: int
    is_game_end: bool
    game_info: GameInfo
    round_info: RoundInfo
    history_updates: list[HistoryItem]
    player_info: PlayerInfo
    win_info: Optional[Win]
    scoring_info: Optional[Scoring]


@final
class GameController:
    def __init__(self, players: list[Player], options: GameOptions) -> None:
        self._players = sample(players, len(players))
        self._game = Game(options=options)
        self._lock = Lock()
        with self._lock:
            self._emit_info_all_inner(self._game.round.history)

    @property
    def game(self) -> Game:
        return self._game

    def emit_info(self, player: Player) -> None:
        with self._lock:
            index = self._get_player_index(player)
            sio.emit("info", self._info(index, []).model_dump(), to=player.id)

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

    def _game_info(self) -> GameInfo:
        return GameInfo(
            players=self._players,
            wind_round=self._game.wind_round,
            sub_round=self._game.sub_round,
            draw_count=self._game.draw_count,
            player_scores=self._game.player_scores,
        )

    def _round_info(self) -> RoundInfo:
        history = [
            HistoryItem(player_index=action[0], action=action[1])
            for action in self._game.round.history
        ]
        hand_counts = [
            len(self._game.round.get_hand(player))
            for player in range(self._game.player_count)
        ]
        discards = self._game.round.discards
        calls = [
            self._game.round.get_calls(player)
            for player in range(self._game.player_count)
        ]
        flowers = [
            self._game.round.get_flowers(player)
            for player in range(self._game.player_count)
        ]
        return RoundInfo(
            tiles_left=self._game.round.tiles_left,
            current_player=self._game.round.current_player,
            status=self._game.round.status,
            hand_counts=hand_counts,
            discards=list(discards),
            calls=calls,
            flowers=flowers,
            history=history,
        )

    def _player_info(self, index: int) -> PlayerInfo:
        hand = list(self._game.round.get_hand(index))
        if self._game.round.status == RoundStatus.END:
            actions = []
        else:
            actions = self._game.round.allowed_actions[index].actions

        action_selected = False
        return PlayerInfo(
            hand=hand,
            last_tile=self._game.round.last_tile,
            actions=actions,
            action_selected=action_selected,
        )

    def _info(self, index: int, history_updates: list[tuple[int, Action]]) -> AllInfo:
        return AllInfo(
            player_count=self._game.player_count,
            player_index=index,
            is_game_end=self._game.is_game_end,
            game_info=self._game_info(),
            round_info=self._round_info(),
            history_updates=[
                HistoryItem(player_index=history_item[0], action=history_item[1])
                for history_item in history_updates
            ],
            player_info=self._player_info(index),
            win_info=self._game.win if self._game.win else None,
            scoring_info=(self._game.scoring if self._game.scoring else None),
        )

    def _emit_info_all_inner(self, history_updates: list[tuple[int, Action]]) -> None:
        for index, player in enumerate(self._players):
            sio.emit(
                "info", self._info(index, history_updates).model_dump(), to=player.id
            )
