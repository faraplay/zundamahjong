from collections import deque
from collections.abc import Sequence, Callable
from enum import Enum

from .exceptions import InvalidMoveException
from .tile import Tile, is_flower
from .deck import Deck
from .discard_pool import DiscardPool
from .hand import Hand
from .action import Action, ActionType, ActionSet, call_action_types
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


_allowed_actions_funcs = {}
_do_action_funcs = {}


def _register_allowed_actions(round_status: RoundStatus):
    def _register_allowed_action_inner(_allowed_actions_func):
        _allowed_actions_funcs[round_status] = _allowed_actions_func
        return _allowed_actions_func

    return _register_allowed_action_inner


def _register_do_action(action_type: ActionType):
    def _register_do_action_inner(_do_action_func):
        _do_action_funcs[action_type] = _do_action_func
        return _do_action_func

    return _register_do_action_inner


class Round:
    def __init__(
        self,
        wind_round: int = 0,
        tiles: list[int] | None = None,
        options: GameOptions = GameOptions(),
        round_end_callback: Callable[[], None] = lambda: None,
    ):
        self._wind_round = wind_round
        self._player_count = options.player_count
        self._options = options
        self._end_callback = round_end_callback
        self._deck = Deck(tiles) if tiles is not None else Deck.shuffled_deck()
        self._discard_pool = DiscardPool()
        self._hands = tuple(Hand(self._deck) for _ in range(self._player_count))
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
    def discards(self):
        return self._discard_pool.discards

    @property
    def discard_tiles(self):
        return [discard.tile for discard in self._discard_pool.discards]

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
        print("Discards:", self.discard_tiles)

    def allowed_actions(self, seat: int):
        return _allowed_actions_funcs[self._status](
            self, seat, self._hands[seat], self._last_tile
        )

    def do_action(self, seat: int, action: Action):
        if action not in self.allowed_actions(seat).actions:
            raise InvalidMoveException()
        _do_action_funcs[action.action_type](self, seat, action.tile)
        self._history.append((seat, action))
        if self._status == RoundStatus.END:
            self._end_callback()

    def get_priority_action(self, actions: Sequence[Action]):
        if len(actions) != self._player_count:
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
        for index in range(1, self._player_count):
            seat = (self._current_seat + index) % self._player_count
            action = valid_actions[seat]
            if action.action_type > best_action.action_type:
                best_action_seat, best_action = seat, action

        return best_action_seat, best_action

    def _previous_seat(self, seat: int):
        return (seat - 1) % self._player_count

    def _next_seat(self, seat: int):
        return (seat + 1) % self._player_count

    @_register_allowed_actions(RoundStatus.START)
    def _allowed_actions_start(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat == seat:
            for tile in hand.tiles:
                if is_flower(tile):
                    actions.add(ActionType.FLOWER, tile)
        return actions

    @_register_allowed_actions(RoundStatus.PLAY)
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

    @_register_allowed_actions(RoundStatus.CALLED_PLAY)
    def _allowed_actions_called_play(self, seat: int, hand: Hand, last_tile: Tile):
        if self._current_seat == seat:
            actions = ActionSet(ActionType.DISCARD, hand.tiles[-1])
            for tile in set(hand.tiles):
                actions.add(ActionType.DISCARD, tile)
        else:
            actions = ActionSet()
        return actions

    @_register_allowed_actions(RoundStatus.ADD_KAN_AFTER)
    def _allowed_actions_add_kan_after(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat != seat:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.CLOSED_KAN_AFTER)
    def _allowed_actions_closed_kan_after(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat != seat:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.DISCARDED)
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

    @_register_allowed_actions(RoundStatus.LAST_DISCARDED)
    def _allowed_actions_last_discarded(self, seat: int, hand: Hand, last_tile: Tile):
        actions = ActionSet()
        if self._current_seat != seat:
            if hand.can_ron(last_tile):
                actions.add(ActionType.RON)
        return actions

    @_register_do_action(ActionType.NOTHING)
    def _nothing(self, seat: int, tile: Tile):
        match self._status:
            case RoundStatus.START:
                self._flower_pass_count += 1
                if self._flower_pass_count >= self._player_count + 1:
                    self._current_seat = 0
                    self._status = RoundStatus.PLAY
                else:
                    self._current_seat = self._next_seat(self._current_seat)
            case RoundStatus.ADD_KAN_AFTER | RoundStatus.CLOSED_KAN_AFTER:
                self._status = RoundStatus.PLAY
                self._last_tile = 0
            case RoundStatus.LAST_DISCARDED:
                self._status = RoundStatus.END

    @_register_do_action(ActionType.DRAW)
    def _draw(self, seat: int, tile: Tile):
        self._hands[seat].draw()
        self._current_seat = seat
        self._status = RoundStatus.PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.DISCARD)
    def _discard(self, seat: int, tile: Tile):
        self._hands[seat].discard(tile)
        self._discard_pool.append(seat, tile)
        if self.wall_count > self._options.end_wall_count:
            self._status = RoundStatus.DISCARDED
        else:
            self._status = RoundStatus.LAST_DISCARDED
        self._last_tile = tile

    @_register_do_action(ActionType.CHI_A)
    def _chi_a(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].chi_a(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.CHI_B)
    def _chi_b(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].chi_b(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.CHI_C)
    def _chi_c(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].chi_c(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.PON)
    def _pon(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].pon(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.OPEN_KAN)
    def _open_kan(self, seat: int, tile: Tile):
        self._discard_pool.pop()
        self._hands[seat].open_kan(self._last_tile)
        self._current_seat = seat
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.ADD_KAN)
    def _add_kan(self, seat: int, tile: Tile):
        self._hands[seat].add_kan(tile)
        self._status = RoundStatus.ADD_KAN_AFTER
        self._last_tile = tile

    @_register_do_action(ActionType.CLOSED_KAN)
    def _closed_kan(self, seat: int, tile: Tile):
        self._hands[seat].closed_kan(tile)
        self._status = RoundStatus.CLOSED_KAN_AFTER
        self._last_tile = tile

    @_register_do_action(ActionType.FLOWER)
    def _flower(self, seat: int, tile: Tile):
        self._hands[seat].flower(tile)
        self._flower_pass_count = 0

    @_register_do_action(ActionType.RON)
    def _ron(self, seat: int, tile: Tile):
        hand = self._hands[seat]
        is_chankan = (
            self._status == RoundStatus.ADD_KAN_AFTER
            or self._status == RoundStatus.CLOSED_KAN_AFTER
        )
        is_houtei = self._status == RoundStatus.LAST_DISCARDED
        self._win_info = Win(
            win_seat=seat,
            lose_seat=self._current_seat,
            hand=list(hand.tiles) + [self._last_tile],
            calls=list(hand.calls),
            wind_round=self._wind_round,
            is_chankan=is_chankan,
            is_houtei=is_houtei,
        )
        self._status = RoundStatus.END

    @_register_do_action(ActionType.TSUMO)
    def _tsumo(self, seat: int, tile: Tile):
        hand = self._hands[seat]
        after_flower_count = 0
        after_kan_count = 0
        for seat, action in reversed(self._history):
            action_type = action.action_type
            if action_type == ActionType.FLOWER:
                after_flower_count += 1
            elif action_type == ActionType.ADD_KAN:
                after_kan_count += 1
            elif action_type == ActionType.CLOSED_KAN:
                after_kan_count += 1
            elif action_type == ActionType.NOTHING:
                pass
            else:
                break
        is_haitei = self.wall_count <= self._options.end_wall_count
        is_tenhou = False
        is_chiihou = False
        if not any(
            (action.action_type in call_action_types)
            or (action.action_type == ActionType.DISCARD and history_seat == seat)
            for history_seat, action in self._history
        ):
            if seat == 0:
                is_tenhou = True
            else:
                is_chiihou = True
        self._win_info = Win(
            win_seat=seat,
            lose_seat=None,
            hand=list(hand.tiles),
            calls=list(hand.calls),
            wind_round=self._wind_round,
            after_flower_count=after_flower_count,
            after_kan_count=after_kan_count,
            is_haitei=is_haitei,
            is_tenhou=is_tenhou,
            is_chiihou=is_chiihou,
        )
        self._status = RoundStatus.END
