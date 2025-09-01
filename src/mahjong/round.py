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


class RoundStatus(Enum):
    START = 0  # Options: nothing, flower
    PLAY = 1  # Options: discard, added kan, closed kan, flower, tsumo
    CALLED_PLAY = 2  # Options: discard
    ADD_KAN_AFTER = 3  # Options: nothing, ron (chankan)
    CLOSED_KAN_AFTER = 4  # Options: nothing, ron (chankan)
    DISCARDED = 5  # Options: draw, chi, pon, open kan, ron
    LAST_DISCARDED = 6  # Options: nothing, ron
    END = 7


class RoundOptions(NamedTuple):
    seat_count: int = 4
    auto_replace_flowers: bool = True
    end_wall_count: int = 14


class InvalidMoveException(Exception):
    pass


class Round:
    def __init__(
        self, tiles: list[int] | None = None, options: RoundOptions = RoundOptions()
    ):
        self._options = options
        self._deck = Deck(tiles) if tiles is not None else Deck.shuffled_deck()
        self._discard_pool = DiscardPool()
        self._hands = tuple(Hand(self._deck) for _ in range(self._options.seat_count))
        for tile_count in [4, 4, 4, 1]:
            for hand in self._hands:
                hand.add_to_hand(tile_count)
        self._hands[0].draw()

        self._current_seat = 0
        self._status = RoundStatus.START
        self._last_tile: Tile = 0
        self._history: deque[tuple[int, Action]] = deque()
        self._win_info = None

        self._flower_pass_count = 0
        if self._options.auto_replace_flowers:
            while self._status == RoundStatus.START:
                seat = self._current_seat
                flowers = self._hands[seat].flowers_in_hand()
                for tile in flowers:
                    self.do_action(
                        seat, Action(action_type=ActionType.FLOWER, tile=tile)
                    )
                self.do_action(seat, Action(action_type=ActionType.NOTHING))

        for hand in self._hands:
            hand.sort()

    def get_hand(self, seat: int):
        return self._hands[seat].tiles

    def get_calls(self, seat: int):
        return self._hands[seat].calls

    @property
    def options(self):
        return self._options

    @property
    def current_seat(self):
        return self._current_seat

    @property
    def status(self):
        return self._status

    @property
    def discard_pool(self):
        return self._discard_pool.tiles

    @property
    def wall_count(self):
        return len(self._deck.tiles)

    @property
    def history(self) -> Sequence[tuple[int, Action]]:
        return self._history

    @property
    def win_info(self):
        return self._win_info

    def display_info(self):
        print(
            f"Current seat: {self.current_seat}, "
            + f"Status: {self.status}, "
            + f"Wall count: {self.wall_count}"
        )
        for seat, hand in enumerate(self._hands):
            print(
                f"Seat {seat}: ",
                hand.tiles,
                [call.tiles for call in hand.calls],
            )
        print("Discards:", self._discard_pool.tiles)

    def allowed_actions(self, seat: int):
        return self._allowed_actions_funcs[self._status](
            self, seat, self._hands[seat], self._last_tile
        )

    def do_action(self, seat: int, action: Action):
        if action not in self.allowed_actions(seat).actions:
            raise InvalidMoveException()
        self._do_action_funcs[action.action_type](self, seat, action.tile)
        self._history.append((seat, action))

    def get_priority_action(self, actions: Sequence[Action]):
        if len(actions) != self._options.seat_count:
            raise Exception("Incorrect number of elements in actions")
        valid_actions: list[Action] = []
        for seat, action in enumerate(actions):
            allowed_actions = self.allowed_actions(seat)
            if action in allowed_actions.actions:
                valid_action = action
            else:
                valid_action = allowed_actions.default
            valid_actions.append(valid_action)

        best_action_seat, best_action = (
            self._current_seat,
            valid_actions[self._current_seat],
        )
        for index in range(1, self._options.seat_count):
            seat = (self._current_seat + index) % self._options.seat_count
            action = valid_actions[seat]
            if action.action_type > best_action.action_type:
                best_action_seat, best_action = seat, action

        return best_action_seat, best_action

    def _previous_seat(self, seat: int):
        return (seat - 1) % self._options.seat_count

    def _next_seat(self, seat: int):
        return (seat + 1) % self._options.seat_count

    def _allowed_actions_start(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat == seat:
            for tile in hand.tiles:
                if is_flower(tile):
                    actions.add(ActionType.FLOWER, tile)
        return actions

    def _allowed_actions_play(self, seat: int, hand: Hand, last_tile: Tile):
        if self._current_seat == seat:
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

    def _allowed_actions_called_play(self, seat: int, hand: Hand, last_tile: Tile):
        if self._current_seat == seat:
            actions = ActionSet(ActionType.DISCARD, hand.tiles[-1])
            for tile in set(hand.tiles):
                actions.add(ActionType.DISCARD, tile)
        else:
            actions = ActionSet()
        return actions

    def _allowed_actions_add_kan_after(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat != seat:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    def _allowed_actions_closed_kan_after(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat != seat:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    def _allowed_actions_discarded(self, seat: int, hand: Hand, last_tile: Tile):
        if self._current_seat == self._previous_seat(seat):
            actions = ActionSet(ActionType.DRAW)
        else:
            actions = ActionSet()
        if self._current_seat == self._previous_seat(seat):
            if hand.can_chi_a(last_tile):
                actions.add(ActionType.CHI_A)
            if hand.can_chi_b(last_tile):
                actions.add(ActionType.CHI_B)
            if hand.can_chi_c(last_tile):
                actions.add(ActionType.CHI_C)
        if self._current_seat != seat:
            if hand.can_pon(last_tile):
                actions.add(ActionType.PON)
            if hand.can_open_kan(last_tile):
                actions.add(ActionType.OPEN_KAN)
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    def _allowed_actions_last_discarded(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat != seat:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    _allowed_actions_funcs = {
        RoundStatus.START: _allowed_actions_start,
        RoundStatus.PLAY: _allowed_actions_play,
        RoundStatus.CALLED_PLAY: _allowed_actions_called_play,
        RoundStatus.ADD_KAN_AFTER: _allowed_actions_add_kan_after,
        RoundStatus.CLOSED_KAN_AFTER: _allowed_actions_closed_kan_after,
        RoundStatus.DISCARDED: _allowed_actions_discarded,
        RoundStatus.LAST_DISCARDED: _allowed_actions_last_discarded,
    }

    def _nothing(self, seat: int, tile: Tile):
        match self._status:
            case RoundStatus.START:
                self._flower_pass_count += 1
                if self._flower_pass_count >= self._options.seat_count + 1:
                    self._current_seat = 0
                    self._status = RoundStatus.PLAY
                else:
                    self._current_seat = self._next_seat(self._current_seat)
            case RoundStatus.ADD_KAN_AFTER | RoundStatus.CLOSED_KAN_AFTER:
                self._status = RoundStatus.PLAY
                self._last_tile = 0
            case RoundStatus.LAST_DISCARDED:
                self._status = RoundStatus.END

    def _draw(self, seat: int, tile: Tile):
        self._hands[seat].draw()
        self._current_seat = seat
        self._status = RoundStatus.PLAY
        self._last_tile = 0

    def _discard(self, seat: int, tile: Tile):
        self._hands[seat].discard(tile)
        self._discard_pool.append(tile)
        if self.wall_count > self._options.end_wall_count:
            self._status = RoundStatus.DISCARDED
        else:
            self._status = RoundStatus.LAST_DISCARDED
        self._last_tile = tile

    def _chi_a(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].chi_a(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    def _chi_b(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].chi_b(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    def _chi_c(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].chi_c(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    def _pon(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].pon(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    def _open_kan(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].open_kan(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    def _add_kan(self, seat: int, tile: Tile):
        self._hands[seat].add_kan(tile)
        self._status = RoundStatus.ADD_KAN_AFTER
        self._last_tile = tile

    def _closed_kan(self, seat: int, tile: Tile):
        self._hands[seat].closed_kan(tile)
        self._status = RoundStatus.CLOSED_KAN_AFTER
        self._last_tile = tile

    def _flower(self, seat: int, tile: Tile):
        self._hands[seat].flower(tile)
        self._flower_pass_count = 0

    def _ron(self, seat: int, tile: Tile):
        hand = self._hands[seat]
        self._win_info = WinInfo(
            win_seat=seat,
            lose_seat=self._current_seat,
            hand=list(hand.tiles) + [self._last_tile],
            calls=list(hand.calls),
        )
        self._status = RoundStatus.END

    def _tsumo(self, seat: int, tile: Tile):
        hand = self._hands[seat]
        self._win_info = WinInfo(
            win_seat=seat, lose_seat=-1, hand=list(hand.tiles), calls=list(hand.calls)
        )
        self._status = RoundStatus.END

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
