from __future__ import annotations
from typing import Optional
from collections import deque
from collections.abc import Sequence, Callable
from enum import Enum


from .exceptions import InvalidMoveException
from .tile import TileId
from .call import get_call_tiles
from .action import (
    Action,
    ActionType,
    ActionList,
    SimpleAction,
    call_action_types,
)
from .deck import Deck, four_player_deck, three_player_deck
from .discard_pool import DiscardPool
from .hand import Hand
from .win import Win
from .game_options import GameOptions


class RoundStatus(Enum):
    START = 0  # Options: nothing, flower
    PLAY = 1  # Options: discard, added kan, closed kan, flower, tsumo
    CALLED_PLAY = 2  # Options: discard
    ADD_KAN_AFTER = 3  # Options: nothing, ron (chankan)
    CLOSED_KAN_AFTER = 4  # Options: nothing, ron (chankan)
    DISCARDED = 5  # Options: draw, chi, pon, open kan, ron
    LAST_DISCARDED = 6  # Options: nothing, ron
    END = 7


_allowed_actions_funcs: dict[
    RoundStatus, Callable[[Round, int, Hand, TileId], ActionList]
] = {}
_do_action_funcs: dict[ActionType, Callable[[Round, int, Action], None]] = {}


def _register_allowed_actions(round_status: RoundStatus):
    def _register_allowed_action_inner(
        _allowed_actions_func: Callable[[Round, int, Hand, TileId], ActionList],
    ):
        _allowed_actions_funcs[round_status] = _allowed_actions_func
        return _allowed_actions_func

    return _register_allowed_action_inner


def _register_do_action(action_type: ActionType):
    def _register_do_action_inner(
        _do_action_func: Callable[[Round, int, Action], None],
    ):
        _do_action_funcs[action_type] = _do_action_func
        return _do_action_func

    return _register_do_action_inner


class Round:
    def __init__(
        self,
        *,
        wind_round: int = 0,
        sub_round: int = 0,
        draw_count: int = 0,
        tiles: Optional[list[TileId]] = None,
        options: GameOptions = GameOptions(),
        round_end_callback: Callable[[], None] = lambda: None,
    ):
        self._wind_round = wind_round
        self._sub_round = sub_round
        self._draw_count = draw_count
        self._player_count = options.player_count
        self._options = options
        self._end_callback = round_end_callback
        if tiles is not None:
            self._deck = Deck(tiles)
        else:
            if options.player_count == 3:
                self._deck = Deck.shuffled_deck(three_player_deck)
            else:
                self._deck = Deck.shuffled_deck(four_player_deck)
        self._discard_pool = DiscardPool()
        self._hands = [Hand(self._deck) for _ in range(self._player_count)]
        for tile_count in [4, 4, 4, 1]:
            for wind in range(self._player_count):
                self._hands[(sub_round + wind) % self._player_count].add_to_hand(
                    tile_count
                )
        self._hands[sub_round].draw()

        for hand in self._hands:
            hand.sort()

        self._current_player = sub_round
        self._status = RoundStatus.START
        self._last_tile: TileId = 0
        self._history: list[tuple[int, Action]] = []
        self._win_info: Optional[Win] = None

        self._calculate_allowed_actions()

        self._flower_pass_count = 0
        if self._options.auto_replace_flowers:
            while self._status == RoundStatus.START:
                player = self._current_player
                flower_actions = self._hands[player].get_flowers()
                for flower_action in flower_actions:
                    self.do_action(player, flower_action)
                self.do_action(player, SimpleAction(action_type=ActionType.CONTINUE))

    def get_hand(self, player: int):
        return self._hands[player].tiles

    def get_discard_tiles(self, player: int):
        return [
            discard.tile
            for discard in self._discard_pool.discards
            if discard.player == player
        ]

    def get_calls(self, player: int):
        return self._hands[player].calls

    def get_flowers(self, player: int):
        return self._hands[player].flowers

    @property
    def options(self):
        return self._options

    @property
    def current_player(self):
        return self._current_player

    @property
    def status(self):
        return self._status

    @property
    def allowed_actions(self):
        return self._allowed_actions

    @property
    def discards(self):
        return self._discard_pool.discards

    @property
    def discard_tiles(self):
        return [discard.tile for discard in self._discard_pool.discards]

    @property
    def last_tile(self):
        return self._last_tile

    @property
    def wall_count(self):
        return len(self._deck.tiles)

    @property
    def tiles_left(self):
        return len(self._deck.tiles) - self._options.end_wall_count

    @property
    def history(self) -> list[tuple[int, Action]]:
        return self._history

    @property
    def win_info(self):
        return self._win_info

    def display_info(self):
        print(
            f"Current player: {self.current_player}, "
            + f"Status: {self.status}, "
            + f"Wall count: {self.wall_count}"
        )
        for player, hand in enumerate(self._hands):
            print(
                f"Player {player}: ",
                hand.tiles,
                [get_call_tiles(call) for call in hand.calls],
            )
        print("Discards:", self.discard_tiles)

    def _calculate_allowed_actions(self):
        self._allowed_actions = tuple(
            _allowed_actions_funcs[self._status](
                self, player, self._hands[player], self._last_tile
            )
            for player in range(self._player_count)
        )
        self._all_allowed_actions = sorted(
            (
                (player, action)
                for player, action_list in enumerate(self._allowed_actions)
                for action in action_list.actions
            ),
            key=lambda playeraction: (
                -playeraction[1].action_type,
                (playeraction[0] - self._current_player) % self._player_count,
            ),
        )

    def do_action(self, player: int, action: Action):
        if action not in self.allowed_actions[player].actions:
            raise InvalidMoveException()
        _do_action_funcs[action.action_type](self, player, action)
        self._history.append((player, action))
        self._calculate_allowed_actions()
        if self._status == RoundStatus.END:
            self._end_callback()

    def get_priority_action(self, actions: Sequence[Optional[Action]]):
        if len(actions) != self._player_count:
            raise Exception("Incorrect number of elements in actions")
        validated_actions: list[Optional[Action]] = []
        for player, action in enumerate(actions):
            allowed_actions = self.allowed_actions[player]
            if action is None:
                valid_action = allowed_actions.auto
            elif action not in allowed_actions.actions:
                valid_action = allowed_actions.default
            else:
                valid_action = action
            validated_actions.append(valid_action)

        for player, action in self._all_allowed_actions:
            if validated_actions[player] == action:
                return player, action
            elif validated_actions[player] is None:
                return None
        assert False

    def _previous_player(self, player: int):
        return (player - 1) % self._player_count

    def _next_player(self, player: int):
        return (player + 1) % self._player_count

    @_register_allowed_actions(RoundStatus.START)
    def _allowed_actions_start(self, player: int, hand: Hand, last_tile: TileId):
        if self._current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
            actions.add_actions(hand.get_flowers())
            return actions
        else:
            return ActionList()

    @_register_allowed_actions(RoundStatus.PLAY)
    def _allowed_actions_play(self, player: int, hand: Hand, last_tile: TileId):
        if self._current_player == player:
            flower_actions = hand.get_flowers()
            if self._options.auto_replace_flowers and len(flower_actions) > 0:
                return ActionList(flower_actions[0])
            else:
                discard_actions = hand.get_discards()
                actions = ActionList(discard_actions[-1])
                actions.add_actions(discard_actions[:-1])
                actions.add_actions(hand.get_add_kans())
                actions.add_actions(hand.get_closed_kans())
                actions.add_actions(flower_actions)
                if hand.can_tsumo():
                    actions.add_simple_action(ActionType.TSUMO)
                return actions
        else:
            return ActionList()

    @_register_allowed_actions(RoundStatus.CALLED_PLAY)
    def _allowed_actions_called_play(self, player: int, hand: Hand, last_tile: TileId):
        if self._current_player == player:
            discard_actions = hand.get_discards()
            actions = ActionList(discard_actions[-1])
            actions.add_actions(discard_actions[:-1])
        else:
            actions = ActionList()
        return actions

    @_register_allowed_actions(RoundStatus.ADD_KAN_AFTER)
    def _allowed_actions_add_kan_after(
        self, player: int, hand: Hand, last_tile: TileId
    ):
        if self.current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
        else:
            actions = ActionList()
            if hand.can_ron(last_tile):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.CLOSED_KAN_AFTER)
    def _allowed_actions_closed_kan_after(
        self, player: int, hand: Hand, last_tile: TileId
    ):
        if self.current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
        else:
            actions = ActionList()
            if hand.can_ron(last_tile):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.DISCARDED)
    def _allowed_actions_discarded(self, player: int, hand: Hand, last_tile: TileId):
        if self._current_player == self._previous_player(player):
            actions = ActionList(SimpleAction(action_type=ActionType.DRAW))
        else:
            actions = ActionList()
        if self._current_player == self._previous_player(player):
            actions.add_actions(hand.get_chiis(last_tile))
        if self._current_player != player:
            actions.add_actions(hand.get_pons(last_tile))
            actions.add_actions(hand.get_open_kans(last_tile))
            if hand.can_ron(last_tile):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.LAST_DISCARDED)
    def _allowed_actions_last_discarded(
        self, player: int, hand: Hand, last_tile: TileId
    ):
        if self.current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
        else:
            actions = ActionList()
            if hand.can_ron(last_tile):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.END)
    def _allowed_actions_end(self, player: int, hand: Hand, last_tile: TileId):
        return ActionList()

    @_register_do_action(ActionType.PASS)
    def _pass(self, player: int, action: Action):
        assert action.action_type == ActionType.PASS
        assert False

    @_register_do_action(ActionType.CONTINUE)
    def _continue(self, player: int, action: Action):
        assert action.action_type == ActionType.CONTINUE
        if self._status == RoundStatus.START:
            self._hands[player].sort()
            self._flower_pass_count += 1
            if self._flower_pass_count >= self._player_count + 1:
                self._current_player = self._sub_round
                self._status = RoundStatus.PLAY
            else:
                self._current_player = self._next_player(self._current_player)
        elif (
            self._status == RoundStatus.ADD_KAN_AFTER
            or self._status == RoundStatus.CLOSED_KAN_AFTER
        ):
            self._status = RoundStatus.PLAY
            self._last_tile = 0
        elif self._status == RoundStatus.LAST_DISCARDED:
            self._status = RoundStatus.END

    @_register_do_action(ActionType.DRAW)
    def _draw(self, player: int, action: Action):
        assert action.action_type == ActionType.DRAW
        self._hands[player].draw()
        self._current_player = player
        self._status = RoundStatus.PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.DISCARD)
    def _discard(self, player: int, action: Action):
        assert action.action_type == ActionType.DISCARD
        tile = action.tile
        self._hands[player].discard(tile)
        self._discard_pool.append(player, tile)
        if self.wall_count > self._options.end_wall_count:
            self._status = RoundStatus.DISCARDED
        else:
            self._status = RoundStatus.LAST_DISCARDED
        self._last_tile = tile

    @_register_do_action(ActionType.CHII)
    def _chii(self, player: int, action: Action):
        assert action.action_type == ActionType.CHII
        self._discard_pool.pop()
        self._hands[player].chii(
            self._current_player, self._last_tile, action.other_tiles
        )
        self._current_player = player
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.PON)
    def _pon(self, player: int, action: Action):
        assert action.action_type == ActionType.PON
        self._discard_pool.pop()
        self._hands[player].pon(
            self._current_player, self._last_tile, action.other_tiles
        )
        self._current_player = player
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.OPEN_KAN)
    def _open_kan(self, player: int, action: Action):
        assert action.action_type == ActionType.OPEN_KAN
        self._discard_pool.pop()
        self._hands[player].open_kan(
            self._current_player, self._last_tile, action.other_tiles
        )
        self._current_player = player
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.ADD_KAN)
    def _add_kan(self, player: int, action: Action):
        assert action.action_type == ActionType.ADD_KAN
        self._hands[player].add_kan(action.tile, action.pon_call)
        self._status = RoundStatus.ADD_KAN_AFTER
        self._last_tile = action.tile

    @_register_do_action(ActionType.CLOSED_KAN)
    def _closed_kan(self, player: int, action: Action):
        assert action.action_type == ActionType.CLOSED_KAN
        self._hands[player].closed_kan(action.tiles)
        self._status = RoundStatus.CLOSED_KAN_AFTER
        self._last_tile = action.tiles[0]

    @_register_do_action(ActionType.FLOWER)
    def _flower(self, player: int, action: Action):
        assert action.action_type == ActionType.FLOWER
        self._hands[player].flower(action.tile)
        self._flower_pass_count = 0

    @_register_do_action(ActionType.RON)
    def _ron(self, player: int, action: Action):
        assert action.action_type == ActionType.RON
        hand = self._hands[player]
        is_chankan = (
            self._status == RoundStatus.ADD_KAN_AFTER
            or self._status == RoundStatus.CLOSED_KAN_AFTER
        )
        is_houtei = self._status == RoundStatus.LAST_DISCARDED
        self._win_info = Win(
            win_player=player,
            lose_player=self._current_player,
            hand=list(hand.tiles) + [self._last_tile],
            calls=list(hand.calls),
            flowers=list(hand.flowers),
            player_count=self._player_count,
            wind_round=self._wind_round,
            sub_round=self._sub_round,
            draw_count=self._draw_count,
            is_chankan=is_chankan,
            is_houtei=is_houtei,
        )
        self._status = RoundStatus.END

    @_register_do_action(ActionType.TSUMO)
    def _tsumo(self, player: int, action: Action):
        assert action.action_type == ActionType.TSUMO
        hand = self._hands[player]
        after_flower_count = 0
        after_kan_count = 0
        for player, action in reversed(self._history):
            action_type = action.action_type
            if action_type == ActionType.FLOWER:
                after_flower_count += 1
            elif action_type == ActionType.ADD_KAN:
                after_kan_count += 1
            elif action_type == ActionType.CLOSED_KAN:
                after_kan_count += 1
            elif action_type == ActionType.CONTINUE:
                pass
            else:
                break
        is_haitei = self.wall_count <= self._options.end_wall_count
        is_tenhou = False
        is_chiihou = False
        if not any(
            (action.action_type in call_action_types)
            or (action.action_type == ActionType.DISCARD and history_player == player)
            for history_player, action in self._history
        ):
            if player == self._sub_round:
                is_tenhou = True
            else:
                is_chiihou = True
        self._win_info = Win(
            win_player=player,
            lose_player=None,
            hand=list(hand.tiles),
            calls=list(hand.calls),
            flowers=list(hand.flowers),
            player_count=self._player_count,
            wind_round=self._wind_round,
            sub_round=self._sub_round,
            draw_count=self._draw_count,
            after_flower_count=after_flower_count,
            after_kan_count=after_kan_count,
            is_haitei=is_haitei,
            is_tenhou=is_tenhou,
            is_chiihou=is_chiihou,
        )
        self._status = RoundStatus.END
