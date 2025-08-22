from enum import Enum

from .tile import Tile
from .deck import Deck
from .discard_pool import DiscardPool
from .hand import Hand
from .action import ActionType, ActionSet


class Status(Enum):
    DRAWING = 0  # at start of game
    PLAY = 1  # Options: discard, added kan, closed kan, flower, tsumo
    CALLED_PLAY = 2  # Options: discard
    DISCARDED = 3  # Options: draw, chi, pon, open kan, ron


class InvalidMoveException(Exception):
    pass


def previous_player(player: int):
    return (player - 1) % 4


class Game:
    def __init__(self, tiles: list[int] | None = None):
        if tiles is None:
            self._deck = Deck.shuffled_deck()
        else:
            self._deck = Deck(tiles)
        self._discard_pool = DiscardPool()
        self._hands = tuple(Hand(self._deck) for _ in range(4))
        for tile_count in [4, 4, 4, 1]:
            for hand in self._hands:
                hand.add_to_hand(tile_count)
        self._current_player = 0
        self._hands[self._current_player].draw()

        while any(hand.has_flowers() for hand in self._hands):
            for hand in self._hands:
                hand.restore_flowers()

        for hand in self._hands:
            hand.sort()

        self._status = Status.PLAY

    def get_hand(self, player: int):
        return self._hands[player].tiles

    def get_calls(self, player: int):
        return self._hands[player].calls

    @property
    def discard_pool(self):
        return self._discard_pool.tiles

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
        hand = self._hands[player]
        if self._status == Status.PLAY:
            if self._current_player == player:
                actions = ActionSet(ActionType.DISCARD, hand.tiles[-1])
                for tile in set(hand.tiles):
                    actions.add(ActionType.DISCARD, tile)
                    if hand.can_add_kan(tile):
                        actions.add(ActionType.ADD_KAN, tile)
                    if hand.can_closed_kan(tile):
                        actions.add(ActionType.CLOSED_KAN, tile)
            else:
                actions = ActionSet()
        elif self._status == Status.CALLED_PLAY:
            if self._current_player == player:
                actions = ActionSet(ActionType.DISCARD, hand.tiles[-1])
                for tile in set(hand.tiles):
                    actions.add(ActionType.DISCARD, tile)
            else:
                actions = ActionSet()
        elif self._status == Status.DISCARDED:
            if self._current_player == previous_player(player):
                actions = ActionSet(ActionType.DRAW)
            else:
                actions = ActionSet()
            last_tile = self._discard_pool.peek()
            if self._current_player == previous_player(player):
                if hand.can_chi_a(last_tile):
                    actions.add(ActionType.CHI_A, last_tile)
                if hand.can_chi_b(last_tile):
                    actions.add(ActionType.CHI_B, last_tile)
                if hand.can_chi_c(last_tile):
                    actions.add(ActionType.CHI_C, last_tile)
            if self._current_player != player:
                if hand.can_pon(last_tile):
                    actions.add(ActionType.PON, last_tile)
                if hand.can_open_kan(last_tile):
                    actions.add(ActionType.OPEN_KAN, last_tile)
        return actions

    def draw(self, player: int):
        hand = self._hands[player]
        if not (
            self._current_player == previous_player(player)
            and self._status == Status.DISCARDED
        ):
            raise InvalidMoveException()
        hand.draw()
        self._current_player = player
        self._status = Status.PLAY

    def discard(self, player: int, tile: int):
        hand = self._hands[player]
        if not (
            self._current_player == player
            and (self._status == Status.PLAY or self._status == Status.CALLED_PLAY)
            and hand.can_discard(tile)
        ):
            raise InvalidMoveException()
        hand.discard(tile)
        self._discard_pool.append(tile)
        self._status = Status.DISCARDED

    def chi_a(self, player: int):
        tile = self._discard_pool.peek()
        hand = self._hands[player]
        if not (
            self._current_player == previous_player(player)
            and self._status == Status.DISCARDED
            and tile != 0
            and hand.can_chi_a(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        hand.chi_a(tile)
        self._current_player = player
        self._status = Status.CALLED_PLAY

    def chi_b(self, player: int):
        tile = self._discard_pool.peek()
        hand = self._hands[player]
        if not (
            self._current_player == previous_player(player)
            and self._status == Status.DISCARDED
            and tile != 0
            and hand.can_chi_b(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        hand.chi_b(tile)
        self._current_player = player
        self._status = Status.CALLED_PLAY

    def chi_c(self, player: int):
        tile = self._discard_pool.peek()
        hand = self._hands[player]
        if not (
            self._current_player == previous_player(player)
            and self._status == Status.DISCARDED
            and tile != 0
            and hand.can_chi_c(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        hand.chi_c(tile)
        self._current_player = player
        self._status = Status.CALLED_PLAY

    def pon(self, player: int):
        tile = self._discard_pool.peek()
        hand = self._hands[player]
        if not (
            self._current_player != player
            and self._status == Status.DISCARDED
            and tile != 0
            and hand.can_pon(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        hand.pon(tile)
        self._current_player = player
        self._status = Status.CALLED_PLAY

    def open_kan(self, player: int):
        tile = self._discard_pool.peek()
        hand = self._hands[player]
        if not (
            self._current_player != player
            and self._status == Status.DISCARDED
            and tile != 0
            and hand.can_open_kan(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        hand.open_kan(tile)
        self._current_player = player
        self._status = Status.CALLED_PLAY

    def add_kan(self, player: int, tile: Tile):
        hand = self._hands[player]
        if not (
            self._current_player == player
            and self._status == Status.PLAY
            and hand.can_add_kan(tile)
        ):
            raise InvalidMoveException()
        hand.add_kan(tile)

    def closed_kan(self, player: int, tile: Tile):
        hand = self._hands[player]
        if not (
            self._current_player == player
            and self._status == Status.PLAY
            and hand.can_closed_kan(tile)
        ):
            raise InvalidMoveException()
        hand.closed_kan(tile)
