from collections.abc import Sequence

from src.mahjong.action import (
    Action,
    ActionType,
    AddKanAction,
    HandTileAction,
    OpenCallAction,
    OpenKanAction,
)

from .tile import (
    TileId,
    TileValue,
    N,
    get_tile_value,
    get_tile_values,
    remove_tile_value,
    tile_id_is_flower,
    is_number,
)
from .deck import Deck
from .call import AddKanCall, CallType, Call, ClosedKanCall, OpenCall, OpenKanCall
from .form_hand import is_winning


class Hand:
    def __init__(self, deck: Deck):
        self._deck = deck
        self._tiles: list[TileId] = []
        self._calls: list[Call] = []
        self._flowers: list[TileId] = []

    @property
    def tiles(self) -> Sequence[TileId]:
        return self._tiles

    @property
    def tile_values(self) -> Sequence[TileValue]:
        return get_tile_values(self._tiles)

    @property
    def calls(self) -> Sequence[Call]:
        return self._calls

    @property
    def flowers(self) -> Sequence[TileId]:
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

    def get_discards(self):
        return [
            HandTileAction(action_type=ActionType.DISCARD, tile=tile)
            for tile in self._tiles
        ]

    def discard(self, tile: TileId):
        self._tiles.remove(tile)
        self.sort()

    def get_chiis(self, last_discard: TileId):
        discard_value = get_tile_value(last_discard)
        actions: list[Action] = []
        if not is_number(discard_value):
            return actions
        # get lists of tiles with values discard_value-2, ..., discard_value+2
        nearby_tiles = [[], [], [], [], []]
        for tile in self._tiles:
            value_diff = get_tile_value(tile) - discard_value
            if -2 <= value_diff <= 2:
                nearby_tiles[value_diff + 2].append(tile)

        if len(nearby_tiles[1]) > 0:
            # note this rules out discard_value = 1, 11, 21
            # try t-2, t-1, t
            if len(nearby_tiles[0]) > 0:
                actions.append(
                    OpenCallAction(
                        action_type=ActionType.CHII,
                        other_tiles=(nearby_tiles[0][0], nearby_tiles[1][0]),
                    )
                )
            # try t-1, t, t+1
            if len(nearby_tiles[3]) > 0:
                actions.append(
                    OpenCallAction(
                        action_type=ActionType.CHII,
                        other_tiles=(nearby_tiles[1][0], nearby_tiles[3][0]),
                    )
                )
        # try t, t+1, t+2
        if len(nearby_tiles[3]) > 0 and len(nearby_tiles[4]) > 0:
            actions.append(
                OpenCallAction(
                    action_type=ActionType.CHII,
                    other_tiles=(nearby_tiles[3][0], nearby_tiles[4][0]),
                )
            )
        return actions

    def chii(
        self,
        called_player_index: int,
        last_discard: TileId,
        other_tiles: tuple[TileId, TileId],
    ):
        self._tiles.remove(other_tiles[0])
        self._tiles.remove(other_tiles[1])
        self._calls.append(
            OpenCall(
                call_type=CallType.CHI,
                called_player_index=called_player_index,
                called_tile=last_discard,
                other_tiles=other_tiles,
            )
        )

    def get_pons(self, last_discard: TileId):
        discard_value = get_tile_value(last_discard)
        actions: list[Action] = []
        same_tiles = [
            tile for tile in self._tiles if get_tile_value(tile) == discard_value
        ]
        if len(same_tiles) >= 2:
            actions.append(
                OpenCallAction(
                    action_type=ActionType.PON,
                    other_tiles=(same_tiles[0], same_tiles[1]),
                )
            )
        return actions

    def pon(
        self,
        called_player_index: int,
        last_discard: TileId,
        other_tiles: tuple[TileId, TileId],
    ):
        self._tiles.remove(other_tiles[0])
        self._tiles.remove(other_tiles[1])
        self._calls.append(
            OpenCall(
                call_type=CallType.PON,
                called_player_index=called_player_index,
                called_tile=last_discard,
                other_tiles=other_tiles,
            )
        )

    def get_open_kans(self, last_discard: TileId):
        discard_value = get_tile_value(last_discard)
        actions: list[Action] = []
        same_tiles = [
            tile for tile in self._tiles if get_tile_value(tile) == discard_value
        ]
        if len(same_tiles) >= 3:
            actions.append(
                OpenKanAction(
                    action_type=ActionType.OPEN_KAN,
                    other_tiles=(same_tiles[0], same_tiles[1], same_tiles[2]),
                )
            )
        return actions

    def open_kan(
        self,
        called_player_index: int,
        last_discard: TileId,
        other_tiles: tuple[TileId, TileId, TileId],
    ):
        self._tiles.remove(other_tiles[0])
        self._tiles.remove(other_tiles[1])
        self._tiles.remove(other_tiles[2])
        self._calls.append(
            OpenKanCall(
                call_type=CallType.OPEN_KAN,
                called_player_index=called_player_index,
                called_tile=last_discard,
                other_tiles=other_tiles,
            )
        )
        self.sort()
        self._draw_from_back()

    def get_add_kans(self):
        pon_values = dict(
            (get_tile_value(call.called_tile), call)
            for call in self._calls
            if call.call_type == CallType.PON
        )
        actions: list[Action] = []
        for tile in self._tiles:
            tile_value = get_tile_value(tile)
            pon_call = pon_values.get(tile_value)
            if pon_call is not None:
                actions.append(AddKanAction(tile=tile, pon_call=pon_call))
        return actions

    def add_kan(self, tile: TileId, pon_call: OpenCall):
        self._tiles.remove(tile)
        call_index = self._calls.index(pon_call)
        self._calls[call_index] = AddKanCall(
            called_player_index=pon_call.called_player_index,
            called_tile=pon_call.called_tile,
            added_tile=tile,
            other_tiles=pon_call.other_tiles,
        )
        self.sort()
        self._draw_from_back()

    def get_closed_kans(self):
        actions: list[Action] = []
        same_tile_count = 1
        for index in range(1, len(self._tiles)):
            if get_tile_value(self._tiles[index]) == get_tile_value(
                self._tiles[index - 1]
            ):
                same_tile_count += 1
                if same_tile_count == 4:
                    actions.append(
                        ClosedKanCall(tiles=self._tiles[index - 3 : index + 1])
                    )
            else:
                same_tile_count = 1
        return actions

    def closed_kan(self, tiles: tuple[TileId, TileId, TileId, TileId]):
        self._tiles.remove(tiles[0])
        self._tiles.remove(tiles[1])
        self._tiles.remove(tiles[2])
        self._tiles.remove(tiles[3])
        self._calls.append(ClosedKanCall(tiles=tiles))
        self.sort()
        self._draw_from_back()

    def get_flowers(self):
        return [
            HandTileAction(action_type=ActionType.FLOWER, tile=tile)
            for tile in self._tiles
            if tile_id_is_flower(tile)
        ]

    def flower(self, tile: TileId):
        self._tiles.remove(tile)
        self._flowers.append(tile)
        self.sort()
        self._draw_from_back()

    def can_ron(self, tile: TileId):
        return is_winning(self._tiles + [tile])

    def can_tsumo(self):
        return is_winning(self._tiles)
