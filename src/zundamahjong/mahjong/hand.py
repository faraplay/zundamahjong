from collections.abc import Sequence

from .tile import (
    Tile,
    TileValue,
    get_tile_values,
    remove_tile_value,
    tile_is_flower,
    is_number,
)
from .deck import Deck
from .call import CallType, Call
from .form_hand import is_winning


class Hand:
    def __init__(self, deck: Deck):
        self._deck = deck
        self._tiles: list[Tile] = []
        self._calls: list[Call] = []
        self._flowers: list[Tile] = []

    @property
    def tiles(self) -> Sequence[Tile]:
        return self._tiles

    @property
    def tile_values(self) -> Sequence[TileValue]:
        return get_tile_values(self._tiles)

    @property
    def calls(self) -> Sequence[Call]:
        return self._calls

    @property
    def flowers(self) -> Sequence[Tile]:
        return self._flowers

    def remove_tile_value(self, tile_value: TileValue):
        return remove_tile_value(self._tiles, tile_value)

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
        tile_value = tile // 4
        return (
            is_number(tile_value)
            and (tile_value + 1) in self.tile_values
            and (tile_value + 2) in self.tile_values
        )

    def chi_a(self, tile: Tile):
        assert self.can_chi_a(tile)
        tile_value = tile // 4
        tile_1 = self.remove_tile_value(tile_value + 1)
        tile_2 = self.remove_tile_value(tile_value + 2)
        self._calls.append(Call(call_type=CallType.CHI, tiles=[tile, tile_1, tile_2]))

    def can_chi_b(self, tile: Tile):
        tile_value = tile // 4
        return (
            is_number(tile_value)
            and (tile_value - 1) in self.tile_values
            and (tile_value + 1) in self.tile_values
        )

    def chi_b(self, tile: Tile):
        assert self.can_chi_b(tile)
        tile_value = tile // 4
        tile_m1 = self.remove_tile_value(tile_value - 1)
        tile_1 = self.remove_tile_value(tile_value + 1)
        self._calls.append(Call(call_type=CallType.CHI, tiles=[tile_m1, tile, tile_1]))

    def can_chi_c(self, tile: Tile):
        tile_value = tile // 4
        return (
            is_number(tile_value)
            and (tile_value - 2) in self.tile_values
            and (tile_value - 1) in self.tile_values
        )

    def chi_c(self, tile: Tile):
        assert self.can_chi_c(tile)
        tile_value = tile // 4
        tile_m2 = self.remove_tile_value(tile_value - 2)
        tile_m1 = self.remove_tile_value(tile_value - 1)
        self._calls.append(Call(call_type=CallType.CHI, tiles=[tile_m2, tile_m1, tile]))

    def can_pon(self, tile: Tile):
        tile_value = tile // 4
        return self.tile_values.count(tile_value) >= 2

    def pon(self, tile: Tile):
        assert self.can_pon(tile)
        tile_value = tile // 4
        tile_a = self.remove_tile_value(tile_value)
        tile_b = self.remove_tile_value(tile_value)
        self._calls.append(Call(call_type=CallType.PON, tiles=[tile, tile_a, tile_b]))

    def can_open_kan(self, tile: Tile):
        tile_value = tile // 4
        return self.tile_values.count(tile_value) >= 3

    def open_kan(self, tile: Tile):
        assert self.can_open_kan(tile)
        tile_value = tile // 4
        tile_a = self.remove_tile_value(tile_value)
        tile_b = self.remove_tile_value(tile_value)
        tile_c = self.remove_tile_value(tile_value)
        self._calls.append(
            Call(call_type=CallType.OPEN_KAN, tiles=[tile, tile_a, tile_b, tile_c])
        )
        self.sort()
        self._draw_from_back()

    def can_add_kan(self, tile: Tile):
        tile_value = tile // 4
        return tile in self._tiles and any(
            call.call_type == CallType.PON and call.tiles[0] // 4 == tile_value
            for call in self._calls
        )

    def add_kan(self, tile: Tile):
        assert self.can_add_kan(tile)
        tile_value = tile // 4
        pon_index, pon_call = next(
            (index, call)
            for index, call in enumerate(self._calls)
            if call.call_type == CallType.PON and call.tiles[0] // 4 == tile_value
        )
        self._tiles.remove(tile)
        self._calls[pon_index] = Call(
            call_type=CallType.ADD_KAN, tiles=[tile] + pon_call.tiles
        )
        self.sort()
        self._draw_from_back()

    def can_closed_kan(self, tile: Tile):
        tile_value = tile // 4
        return tile % 4 == 0 and self.tile_values.count(tile_value) >= 4

    def closed_kan(self, tile: Tile):
        assert self.can_closed_kan(tile)
        self._tiles.remove(tile)
        self._tiles.remove(tile + 1)
        self._tiles.remove(tile + 2)
        self._tiles.remove(tile + 3)
        self._calls.append(
            Call(
                call_type=CallType.CLOSED_KAN,
                tiles=[tile, tile + 1, tile + 2, tile + 3],
            )
        )
        self.sort()
        self._draw_from_back()

    def can_ron(self, tile: Tile):
        return is_winning(self._tiles + [tile])

    def can_tsumo(self):
        return is_winning(self._tiles)

    def flowers_in_hand(self):
        return [tile for tile in self._tiles if tile_is_flower(tile)]

    def flower(self, tile: Tile):
        assert tile_is_flower(tile)
        assert tile in self._tiles
        self._tiles.remove(tile)
        self._flowers.append(tile)
        self.sort()
        self._draw_from_back()
