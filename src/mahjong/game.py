from enum import Enum

from .tile import Tile
from .deck import Deck
from .discard_pool import DiscardPool
from .hand import Hand


class Status(Enum):
    DRAWING = 0  # at start of game
    PLAY = 1  # Options: discard, added kan, closed kan, flower, tsumo
    DISCARDED = 2  # Options: draw, chi, pon, open kan, ron


class InvalidMoveException(Exception):
    pass


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

    def display_info(self):
        print(f"Current player: {self._current_player}, Status: {self._status}")
        for player, hand in enumerate(self._hands):
            print(
                f"Player {player}: ",
                hand.tiles,
                [call.tiles for call in hand.calls],
            )
        print("Discards:", self._discard_pool.tiles)

    def draw(self, player: int):
        if (self._current_player + 1) % 4 != player or self._status != Status.DISCARDED:
            raise InvalidMoveException()
        self._hands[player].draw()
        self._current_player = player
        self._status = Status.PLAY

    def discard(self, player: int, tile_index: int):
        if player != self._current_player or self._status != Status.PLAY:
            raise InvalidMoveException()
        self._hands[player].discard(tile_index, self._discard_pool)
        self._status = Status.DISCARDED

    def chi_a(self, player: int):
        tile = self._discard_pool.peek()
        if not (
            (self._current_player + 1) % 4 == player
            and self._status == Status.DISCARDED
            and tile != 0
            and self._hands[player].can_chi_a(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        self._hands[player].chi_a(tile)
        self._current_player = player
        self._status = Status.PLAY

    def chi_b(self, player: int):
        tile = self._discard_pool.peek()
        if not (
            (self._current_player + 1) % 4 == player
            and self._status == Status.DISCARDED
            and tile != 0
            and self._hands[player].can_chi_b(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        self._hands[player].chi_b(tile)
        self._current_player = player
        self._status = Status.PLAY

    def chi_c(self, player: int):
        tile = self._discard_pool.peek()
        if not (
            (self._current_player + 1) % 4 == player
            and self._status == Status.DISCARDED
            and tile != 0
            and self._hands[player].can_chi_c(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        self._hands[player].chi_c(tile)
        self._current_player = player
        self._status = Status.PLAY

    def pon(self, player: int):
        tile = self._discard_pool.peek()
        if not (
            player != self._current_player
            and self._status == Status.DISCARDED
            and tile != 0
            and self._hands[player].can_pon(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        self._hands[player].pon(tile)
        self._current_player = player
        self._status = Status.PLAY

    def open_kan(self, player: int):
        tile = self._discard_pool.peek()
        if not (
            player != self._current_player
            and self._status == Status.DISCARDED
            and tile != 0
            and self._hands[player].can_open_kan(tile)
        ):
            raise InvalidMoveException()
        self._discard_pool.pop()
        self._hands[player].kan(tile)
        self._current_player = player
        self._status = Status.PLAY

    def add_kan(self, player: int, tile: Tile):
        if not (
            player == self._current_player
            and self._status == Status.PLAY
            and self._hands[player].can_add_kan(tile)
        ):
            raise InvalidMoveException()
        self._hands[player].add_kan(tile)

    def closed_kan(self, player: int, tile: Tile):
        if not (
            player == self._current_player
            and self._status == Status.PLAY
            and self._hands[player].can_closed_kan(tile)
        ):
            raise InvalidMoveException()
        self._hands[player].closed_kan(tile)
