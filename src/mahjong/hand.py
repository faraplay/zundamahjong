from collections.abc import Sequence

from .tile import Tile, is_flower, is_number
from .deck import Deck
from .call import CallType, Call
from .form_hand import is_winning


class Hand:
    def __init__(self, deck: Deck):
        self._deck = deck
        self._tiles: list[Tile] = []
        self._calls: list[Call] = []

    @property
    def tiles(self) -> Sequence[Tile]:
        return self._tiles

    @property
    def calls(self) -> Sequence[Call]:
        return self._calls

    def sort(self):
        self._tiles.sort()

    def add_to_hand(self, tile_count: int):
        assert tile_count >= 0
        self._tiles.extend(self._deck.pop() for _ in range(tile_count))

    def draw(self):
        self._tiles.append(self._deck.pop())

    def _draw_from_back(self):
        self._tiles.append(self._deck.popleft())

    def can_discard(self, tile: Tile):
        return tile in self._tiles

    def discard(self, tile: Tile):
        assert self.can_discard(tile)
        self._tiles.remove(tile)
        self.sort()

    def can_chi_a(self, tile: Tile):
        return (
            is_number(tile) and (tile + 1) in self._tiles and (tile + 2) in self._tiles
        )

    def chi_a(self, tile: Tile):
        assert self.can_chi_a(tile)
        self._tiles.remove(tile + 1)
        self._tiles.remove(tile + 2)
        self._calls.append(Call(CallType.CHI, [tile, tile + 1, tile + 2]))

    def can_chi_b(self, tile: Tile):
        return (
            is_number(tile) and (tile - 1) in self._tiles and (tile + 1) in self._tiles
        )

    def chi_b(self, tile: Tile):
        assert self.can_chi_b(tile)
        self._tiles.remove(tile - 1)
        self._tiles.remove(tile + 1)
        self._calls.append(Call(CallType.CHI, [tile - 1, tile, tile + 1]))

    def can_chi_c(self, tile: Tile):
        return (
            is_number(tile) and (tile - 2) in self._tiles and (tile - 1) in self._tiles
        )

    def chi_c(self, tile: Tile):
        assert self.can_chi_c(tile)
        self._tiles.remove(tile - 2)
        self._tiles.remove(tile - 1)
        self._calls.append(Call(CallType.CHI, [tile - 2, tile - 1, tile]))

    def can_pon(self, tile: Tile):
        return self._tiles.count(tile) >= 2

    def pon(self, tile: Tile):
        assert self.can_pon(tile)
        self._tiles.remove(tile)
        self._tiles.remove(tile)
        self._calls.append(Call(CallType.PON, [tile, tile, tile]))

    def can_open_kan(self, tile: Tile):
        return self._tiles.count(tile) >= 3

    def open_kan(self, tile: Tile):
        assert self.can_open_kan(tile)
        self._tiles.remove(tile)
        self._tiles.remove(tile)
        self._tiles.remove(tile)
        self._calls.append(Call(CallType.OPEN_KAN, [tile, tile, tile, tile]))
        self.sort()
        self._draw_from_back()

    def can_add_kan(self, tile: Tile):
        pon_call = Call(CallType.PON, [tile, tile, tile])
        return tile in self._tiles and pon_call in self._calls

    def add_kan(self, tile: Tile):
        assert self.can_add_kan(tile)
        pon_call = Call(CallType.PON, [tile, tile, tile])
        self._tiles.remove(tile)
        pon_index = self._calls.index(pon_call)
        self._calls[pon_index] = Call(CallType.ADD_KAN, [tile, tile, tile, tile])
        self.sort()
        self._draw_from_back()

    def can_closed_kan(self, tile: Tile):
        return self._tiles.count(tile) >= 4

    def closed_kan(self, tile: Tile):
        assert self.can_closed_kan(tile)
        self._tiles.remove(tile)
        self._tiles.remove(tile)
        self._tiles.remove(tile)
        self._tiles.remove(tile)
        self._calls.append(Call(CallType.CLOSED_KAN, [tile, tile, tile, tile]))
        self.sort()
        self._draw_from_back()

    def can_ron(self, tile: Tile):
        return is_winning(self._tiles + [tile])

    def can_tsumo(self):
        return is_winning(self._tiles)

    def has_flowers(self):
        return any(is_flower(tile) for tile in self._tiles)

    def restore_flowers(self):
        flower_count = 0
        for tile in self._tiles:
            if is_flower(tile):
                flower_count += 1
                self._calls.append(Call(CallType.FLOWER, [tile]))
        self._tiles = [tile for tile in self._tiles if not is_flower(tile)]
        for _ in range(flower_count):
            self._draw_from_back()
