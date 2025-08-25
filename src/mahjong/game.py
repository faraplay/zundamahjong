from collections import deque
from collections.abc import Sequence
from enum import Enum
from typing import NamedTuple

from .tile import Tile, is_flower
from .deck import Deck
from .discard_pool import DiscardPool
from .hand import Hand
from .action import Action, ActionType, ActionSet
from .win_info import WinInfo


class GameStatus(Enum):
    START = 0  # Options: nothing, flower
    PLAY = 1  # Options: discard, added kan, closed kan, flower, tsumo
    CALLED_PLAY = 2  # Options: discard
    ADD_KAN_AFTER = 3  # Options: nothing, ron (chankan)
    CLOSED_KAN_AFTER = 4  # Options: nothing, ron (chankan)
    DISCARDED = 5  # Options: draw, chi, pon, open kan, ron
    END = 6


class GameOptions(NamedTuple):
    auto_replace_flowers: bool = True


class InvalidMoveException(Exception):
    pass


class Game:
    def __init__(
        self, tiles: list[int] | None = None, options: GameOptions = GameOptions()
    ):
        self._options = options
        self._deck = Deck(tiles) if tiles is not None else Deck.shuffled_deck()
        self._discard_pool = DiscardPool()
        self._hands = tuple(Hand(self._deck) for _ in range(4))
        for tile_count in [4, 4, 4, 1]:
            for hand in self._hands:
                hand.add_to_hand(tile_count)
        self._hands[0].draw()

        self._current_player = 0
        self._status = GameStatus.START
        self._last_tile: Tile = 0
        self._history: deque[tuple[int, Action]] = deque()
        self._win_info = None

        self._flower_pass_count = 0
        if self._options.auto_replace_flowers:
            while self._status == GameStatus.START:
                player = self._current_player
                flowers = self._hands[player].flowers_in_hand()
                for tile in flowers:
                    self.do_action(player, Action(ActionType.FLOWER, tile))
                self.do_action(player, Action(ActionType.NOTHING))

    def get_hand(self, player: int):
        return self._hands[player].tiles

    def get_calls(self, player: int):
        return self._hands[player].calls

    @property
    def current_player(self):
        return self._current_player

    @property
    def status(self):
        return self._status

    @property
    def discard_pool(self):
        return self._discard_pool.tiles

    @property
    def history(self) -> Sequence[tuple[int, Action]]:
        return self._history

    @property
    def win_info(self):
        return self._win_info

    def display_info(self):
        print(f"Current player: {self._current_player}, Status: {self._status}")
        for player, hand in enumerate(self._hands):
            print(
                f"Player {player}: ",
                hand.tiles,
                [call.tiles for call in hand.calls],
            )
        print("Discards:", self._discard_pool.tiles)

    def allowed_actions(self, player: int):
        return self._allowed_actions_funcs[self._status](
            self, player, self._hands[player], self._last_tile
        )

    def do_action(self, player: int, action: Action):
        if action not in self.allowed_actions(player).actions:
            raise InvalidMoveException()
        self._do_action_funcs[action.action_type](self, player, action.tile)
        self._history.append((player, action))

    def previous_player(self, player: int):
        return (player - 1) % 4

    def next_player(self, player: int):
        return (player + 1) % 4

    def _allowed_actions_start(self, player: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_player == player:
            for tile in hand.tiles:
                if is_flower(tile):
                    actions.add(ActionType.FLOWER, tile)
        return actions

    def _allowed_actions_play(self, player: int, hand: Hand, last_tile: Tile):
        if self._current_player == player:
            flowers = hand.flowers_in_hand()
            if self._options.auto_replace_flowers and len(flowers) > 0:
                return ActionSet(ActionType.FLOWER, flowers[0])
            else:
                actions = ActionSet(ActionType.DISCARD, hand.tiles[-1])
                for tile in set(hand.tiles):
                    actions.add(ActionType.DISCARD, tile)
                    if hand.can_add_kan(tile):
                        actions.add(ActionType.ADD_KAN, tile)
                    if hand.can_closed_kan(tile):
                        actions.add(ActionType.CLOSED_KAN, tile)
                    if is_flower(tile):
                        actions.add(ActionType.FLOWER, tile)
                if hand.can_tsumo():
                    actions.add(ActionType.TSUMO)
                return actions
        else:
            return ActionSet()

    def _allowed_actions_called_play(self, player: int, hand: Hand, last_tile: Tile):
        if self._current_player == player:
            actions = ActionSet(ActionType.DISCARD, hand.tiles[-1])
            for tile in set(hand.tiles):
                actions.add(ActionType.DISCARD, tile)
        else:
            actions = ActionSet()
        return actions

    def _allowed_actions_add_kan_after(self, player: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_player != player:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    def _allowed_actions_closed_kan_after(
        self, player: int, hand: Hand, last_tile: Tile
    ):
        actions = ActionSet()
        if self._current_player != player:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    def _allowed_actions_discarded(self, player: int, hand: Hand, last_tile: Tile):
        if self._current_player == self.previous_player(player):
            actions = ActionSet(ActionType.DRAW)
        else:
            actions = ActionSet()
        if self._current_player == self.previous_player(player):
            if hand.can_chi_a(last_tile):
                actions.add(ActionType.CHI_A)
            if hand.can_chi_b(last_tile):
                actions.add(ActionType.CHI_B)
            if hand.can_chi_c(last_tile):
                actions.add(ActionType.CHI_C)
        if self._current_player != player:
            if hand.can_pon(last_tile):
                actions.add(ActionType.PON)
            if hand.can_open_kan(last_tile):
                actions.add(ActionType.OPEN_KAN)
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    _allowed_actions_funcs = {
        GameStatus.START: _allowed_actions_start,
        GameStatus.PLAY: _allowed_actions_play,
        GameStatus.CALLED_PLAY: _allowed_actions_called_play,
        GameStatus.ADD_KAN_AFTER: _allowed_actions_add_kan_after,
        GameStatus.CLOSED_KAN_AFTER: _allowed_actions_closed_kan_after,
        GameStatus.DISCARDED: _allowed_actions_discarded,
    }

    def _nothing(self, player: int, tile: Tile):
        match self._status:
            case GameStatus.START:
                self._flower_pass_count += 1
                if self._flower_pass_count >= 4:
                    self._current_player = 0
                    self._status = GameStatus.PLAY
                else:
                    self._current_player = self.next_player(self._current_player)
            case GameStatus.ADD_KAN_AFTER | GameStatus.CLOSED_KAN_AFTER:
                self._status = GameStatus.PLAY
                self._last_tile = 0

    def _draw(self, player: int, tile: Tile):
        self._hands[player].draw()
        self._current_player = player
        self._status = GameStatus.PLAY
        self._last_tile = 0

    def _discard(self, player: int, tile: Tile):
        self._hands[player].discard(tile)
        self._discard_pool.append(tile)
        self._status = GameStatus.DISCARDED
        self._last_tile = tile

    def _chi_a(self, player: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[player].chi_a(self._last_tile)
        self._current_player = player
        self._status = GameStatus.CALLED_PLAY
        self._last_tile = 0

    def _chi_b(self, player: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[player].chi_b(self._last_tile)
        self._current_player = player
        self._status = GameStatus.CALLED_PLAY
        self._last_tile = 0

    def _chi_c(self, player: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[player].chi_c(self._last_tile)
        self._current_player = player
        self._status = GameStatus.CALLED_PLAY
        self._last_tile = 0

    def _pon(self, player: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[player].pon(self._last_tile)
        self._current_player = player
        self._status = GameStatus.CALLED_PLAY
        self._last_tile = 0

    def _open_kan(self, player: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[player].open_kan(self._last_tile)
        self._current_player = player
        self._status = GameStatus.CALLED_PLAY
        self._last_tile = 0

    def _add_kan(self, player: int, tile: Tile):
        self._hands[player].add_kan(tile)
        self._status = GameStatus.ADD_KAN_AFTER
        self._last_tile = tile

    def _closed_kan(self, player: int, tile: Tile):
        self._hands[player].closed_kan(tile)
        self._status = GameStatus.CLOSED_KAN_AFTER
        self._last_tile = tile

    def _flower(self, player: int, tile: Tile):
        self._hands[player].flower(tile)
        self._flower_pass_count = 0

    def _ron(self, player: int, tile: Tile):
        hand = self._hands[player]
        self._win_info = WinInfo(
            player,
            self._current_player,
            list(hand.tiles) + [self._last_tile],
            list(hand.calls),
        )
        self._status = GameStatus.END

    def _tsumo(self, player: int, tile: Tile):
        hand = self._hands[player]
        self._win_info = WinInfo(player, -1, list(hand.tiles), list(hand.calls))
        self._status = GameStatus.END

    _do_action_funcs = {
        ActionType.NOTHING: _nothing,
        ActionType.DRAW: _draw,
        ActionType.DISCARD: _discard,
        ActionType.CHI_A: _chi_a,
        ActionType.CHI_B: _chi_b,
        ActionType.CHI_C: _chi_c,
        ActionType.PON: _pon,
        ActionType.OPEN_KAN: _open_kan,
        ActionType.ADD_KAN: _add_kan,
        ActionType.CLOSED_KAN: _closed_kan,
        ActionType.FLOWER: _flower,
        ActionType.RON: _ron,
        ActionType.TSUMO: _tsumo,
    }
