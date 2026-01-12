from collections.abc import Sequence
from typing import final

from .action import (
    Action,
    ActionType,
    AddKanAction,
    ClosedKanAction,
    HandTileAction,
    OpenCallAction,
    OpenKanAction,
)
from .call import (
    AddKanCall,
    Call,
    CallType,
    ClosedKanCall,
    OpenCall,
    OpenKanCall,
    get_call_tiles,
)
from .deck import Deck
from .discard_pool import DiscardPool
from .form_hand import is_winning
from .shanten import get_waits
from .tile import (
    TileId,
    TileValue,
    get_tile_value,
    get_tile_value_buckets,
    get_tile_values,
    is_number,
    tile_id_is_flower,
)


@final
class Hand:
    """
    Represents a player's hand in a round of mahjong.

    :param deck: The deck for the current round of mahjong. The hand will
                 draw tiles from this deck.
    """

    def __init__(
        self, player_index: int, deck: Deck, discard_pool: DiscardPool
    ) -> None:
        self._player_index = player_index
        self._deck = deck
        self._discard_pool = discard_pool
        self._tiles: list[TileId] = []
        self._calls: list[Call] = []
        self._flowers: list[TileId] = []
        self._waits: frozenset[TileValue] | None = None
        self._riichi_discard_index: int | None = None

    @property
    def tiles(self) -> Sequence[TileId]:
        """
        Return a sequence of :py:class:`TileId` s of the tiles in the player's
        hand (does not include flowers or tiles in calls).
        """
        return self._tiles

    @property
    def tile_values(self) -> Sequence[TileValue]:
        """
        Return a sequence of :py:class:`TileValue` s of the tiles in the player's
        hand (does not include flowers or tiles in calls).
        """
        return get_tile_values(self._tiles)

    @property
    def is_riichi(self) -> bool:
        """
        Return a bool indicating whether the hand has called riichi.
        """
        return self._riichi_discard_index is not None

    @property
    def riichi_discard_index(self) -> int | None:
        """
        Return the number of discards made before the hand called riichi,
        or ``None`` if the hand has not called riichi.

        :param player: The index of the player to check.
        """
        return self._riichi_discard_index

    @property
    def calls(self) -> Sequence[Call]:
        """
        Return a sequence of the player's :py:class:`Call` s.
        """
        return self._calls

    @property
    def call_tiles(self) -> list[TileId]:
        """
        Return a list of :py:class:`TileId` s of the tiles in the player's calls.
        """
        return [tile for call in self._calls for tile in get_call_tiles(call)]

    @property
    def flowers(self) -> Sequence[TileId]:
        """
        Return a sequence of :py:class:`TileId` s of the player's flowers.
        """
        return self._flowers

    def sort(self) -> None:
        "Sort the hand's tiles in ascending order of :py:class:`TileId` ."
        self._tiles.sort()

    def add_to_hand(self, tile_count: int) -> None:
        """
        Draw tiles from the deck and add them to the hand.

        :param tile_count: The number of tiles to draw (must be >= 0).
        """
        assert tile_count >= 0
        self._tiles.extend(self._deck.pop() for _ in range(tile_count))
        self._waits = None

    def draw(self) -> None:
        "Draw a tile from the deck and add it to the hand."
        self._tiles.append(self._deck.pop())
        self._waits = None

    def _draw_from_back(self) -> None:
        "Draw a tile from the back of the deck and add it to the hand."
        self._tiles.append(self._deck.popleft())

    def get_discards(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal discard actions.

        If the hand has riichi'd, then this is just the last drawn tile.
        Otherwise, every tile can be discarded.
        """
        if self.is_riichi:
            return [
                HandTileAction(action_type=ActionType.DISCARD, tile=self._tiles[-1])
            ]
        return [
            HandTileAction(action_type=ActionType.DISCARD, tile=tile)
            for tile in self._tiles
        ]

    def discard(self, tile: TileId) -> None:
        """
        Discard the tile with the specified :py:class:`TileId` .

        :param tile: The :py:class:`TileId` of the tile to discard.
        """
        self._tiles.remove(tile)
        self._discard_pool.append(self._player_index, tile)
        self.sort()
        self._waits = None

    def get_riichis(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal riichi actions.

        If the hand has no open calls and has not riichi'd, then this will
        consist of discards that put the hand into tenpai.
        Otherwise, no riichi actions are allowed.
        """
        if self.is_riichi or not all(
            call.call_type == CallType.CLOSED_KAN for call in self._calls
        ):
            return []
        return [
            HandTileAction(action_type=ActionType.RIICHI, tile=tile)
            for index, tile in enumerate(self._tiles)
            if len(
                get_waits(
                    get_tile_values(self._tiles[:index] + self._tiles[index + 1 :])
                )
            )
            > 0
        ]

    def riichi(self, tile: TileId) -> None:
        """
        Call riichi, discarding the tile with the specified :py:class:`TileId` .

        :param tile: The :py:class:`TileId` of the tile to discard.
        """
        self._tiles.remove(tile)
        self._riichi_discard_index = len(self._discard_pool.discards)
        self._discard_pool.append(self._player_index, tile)
        self.sort()
        self._waits = None

    def get_chiis(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal chii actions.

        :param last_discard: The :py:class:`TileId` of the last discarded tile.
        """
        actions: list[Action] = []
        if self.is_riichi:
            return actions

        last_discarded_tile = self._discard_pool.last_discarded_tile
        if last_discarded_tile is None:
            return actions
        discard_value = get_tile_value(last_discarded_tile)
        if not is_number(discard_value):
            return actions
        # get lists of tiles with values discard_value-2, ..., discard_value+2
        nearby_tiles: list[list[TileId]] = [[], [], [], [], []]
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
        other_tiles: tuple[TileId, TileId],
    ) -> None:
        """
        Form a chii :py:class:`OpenCall` with the last discarded tile
        and add it to the hand's list of calls.

        :param called_player_index: The index of the player who discarded the
                                    last tile.
        :param other_tiles: The tiles in the hand that are used to form a chii
                            :py:class:`OpenCall` with the last discarded tile.
        """
        self._tiles.remove(other_tiles[0])
        self._tiles.remove(other_tiles[1])
        self._calls.append(
            OpenCall(
                call_type=CallType.CHI,
                called_player_index=called_player_index,
                called_tile=self._discard_pool.pop(),
                other_tiles=other_tiles,
            )
        )
        self._waits = None

    def get_pons(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal pon actions.

        :param last_discard: The :py:class:`TileId` of the last discarded tile.
        """
        actions: list[Action] = []
        if self.is_riichi:
            return actions

        last_discarded_tile = self._discard_pool.last_discarded_tile
        if last_discarded_tile is None:
            return actions
        discard_value = get_tile_value(last_discarded_tile)
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
        other_tiles: tuple[TileId, TileId],
    ) -> None:
        """
        Form a pon :py:class:`OpenCall` with the last discarded tile
        and add it to the hand's list of calls.

        :param called_player_index: The index of the player who discarded the
                                    last tile.
        :param other_tiles: The tiles in the hand that are used to form a pon
                            :py:class:`OpenCall` with the last discarded tile.
        """
        self._tiles.remove(other_tiles[0])
        self._tiles.remove(other_tiles[1])
        self._calls.append(
            OpenCall(
                call_type=CallType.PON,
                called_player_index=called_player_index,
                called_tile=self._discard_pool.pop(),
                other_tiles=other_tiles,
            )
        )
        self._waits = None

    def get_open_kans(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal open kan actions.

        :param last_discard: The :py:class:`TileId` of the last discarded tile.
        """
        actions: list[Action] = []
        if self.is_riichi:
            return actions

        last_discarded_tile = self._discard_pool.last_discarded_tile
        if last_discarded_tile is None:
            return actions
        discard_value = get_tile_value(last_discarded_tile)
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
        other_tiles: tuple[TileId, TileId, TileId],
    ) -> None:
        """
        Form an :py:class:`OpenKanCall` with the last discarded tile
        and add it to the hand's list of calls. Then draw a bonus tile
        from the back of the deck.

        :param called_player_index: The index of the player who discarded the
                                    last tile.
        :param other_tiles: The tiles in the hand that are used to form an
                            :py:class:`OpenKanCall` with the last discarded tile.
        """
        self._tiles.remove(other_tiles[0])
        self._tiles.remove(other_tiles[1])
        self._tiles.remove(other_tiles[2])
        self._calls.append(
            OpenKanCall(
                call_type=CallType.OPEN_KAN,
                called_player_index=called_player_index,
                called_tile=self._discard_pool.pop(),
                other_tiles=other_tiles,
            )
        )
        self.sort()
        self._draw_from_back()
        self._waits = None

    def get_add_kans(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal added kan actions.
        """
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

    def add_kan(self, tile: TileId, pon_call: OpenCall) -> None:
        """
        Form an :py:class:`AddKanCall` with an existing pon :py:class:`OpenCall`
        and a tile in the hand, and replace the pon :py:class:`OpenCall`
        with this new :py:class:`AddKanCall` . Then draw a bonus tile
        from the back of the deck.

        :param tile: The :py:class:`TileId` of the tile to add to the
                     pon :py:class:`OpenCall`.
        :param pon_call: The existing pon :py:class:`OpenCall`.
        """
        self._tiles.remove(tile)
        call_index = self._calls.index(pon_call)
        self._calls[call_index] = AddKanCall(
            called_player_index=pon_call.called_player_index,
            called_tile=pon_call.called_tile,
            added_tile=tile,
            other_tiles=pon_call.other_tiles,
        )
        self._discard_pool.append(self._player_index, tile, is_added_kan=True)
        self.sort()
        self._draw_from_back()
        self._waits = None

    def get_closed_kans(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal closed kan actions.
        """
        tile_value_buckets = get_tile_value_buckets(self._tiles)
        if self.is_riichi:
            last_tile_value = get_tile_value(self._tiles[-1])
            bucket = tile_value_buckets[last_tile_value]
            if len(bucket) >= 4:
                kan_tiles = (bucket[0], bucket[1], bucket[2], bucket[3])
                current_waits = self._calculate_waits(self._tiles[:-1])
                tiles_copy = self._tiles.copy()
                for tile in kan_tiles:
                    tiles_copy.remove(tile)
                new_waits = self._calculate_waits(tiles_copy)
                if current_waits == new_waits:
                    return [ClosedKanAction(tiles=kan_tiles)]
            return []
        actions: list[Action] = []
        for bucket in tile_value_buckets.values():
            if len(bucket) >= 4:
                bucket.sort()
                actions.append(
                    ClosedKanAction(tiles=(bucket[0], bucket[1], bucket[2], bucket[3]))
                )
        return actions

    def closed_kan(self, tiles: tuple[TileId, TileId, TileId, TileId]) -> None:
        """
        Form a :py:class:`ClosedKanCall` using four tiles from the hand.
        Then draw a bonus tile from the back of the deck.

        :param tiles: A tuple of the :py:class:`TileId` s of the four tiles
                      used to make the closed kan.
        """
        self._tiles.remove(tiles[0])
        self._tiles.remove(tiles[1])
        self._tiles.remove(tiles[2])
        self._tiles.remove(tiles[3])
        self._calls.append(ClosedKanCall(tiles=tiles))
        self._discard_pool.append(self._player_index, tiles[0], is_closed_kan=True)
        self.sort()
        self._draw_from_back()
        self._waits = None

    def get_flowers(self) -> list[Action]:
        """
        Return a list of :py:class:`Action` s of the hand's legal flower actions.
        """
        return [
            HandTileAction(action_type=ActionType.FLOWER, tile=tile)
            for tile in self._tiles
            if tile_id_is_flower(tile)
        ]

    def flower(self, tile: TileId) -> None:
        """
        Move a flower from the hand's tiles to the hand's list of flowers.
        Then draw a bonus tile from the back of the deck.

        :param tile: The :py:class:`TileId` of the flower in the hand.
        """
        self._tiles.remove(tile)
        self._flowers.append(tile)
        self.sort()
        self._draw_from_back()
        self._waits = None

    def can_tsumo(self) -> bool:
        """
        Return a bool indicating whether the hand forms a winning shape.
        """
        return is_winning(self._tiles)

    @property
    def waits(self) -> frozenset[TileValue]:
        """
        Return a frozenset of the :py:class:`TileValue` s that this hand
        needs to form a winning shape.

        This frozenset of the hand's waits is cached so that it is not
        recalculated if the hand has not changed.
        """
        if self._waits is None:
            self._waits = self._calculate_waits(self._tiles)
        return self._waits

    def _calculate_waits(self, hand_tiles: list[TileId]) -> frozenset[TileValue]:
        if len(hand_tiles) % 3 != 1:
            return frozenset()
        all_tiles_buckets = get_tile_value_buckets(hand_tiles + self.call_tiles)
        unusable_tile_values = {
            tileValue
            for (tileValue, tiles) in all_tiles_buckets.items()
            if len(tiles) >= 4
        }
        waits = get_waits(get_tile_values(hand_tiles))
        return waits - unusable_tile_values

    @property
    def is_temporary_furiten(self) -> bool:
        """
        Whether any old discard since the player's last discard is
        one of the hand's waits.
        """
        for discard in reversed(self._discard_pool.discards):
            if discard.player == self._player_index:
                break
            if discard.is_new:
                continue
            if discard.is_closed_kan:
                continue
            if get_tile_value(discard.tile) in self.waits:
                return True
        return False

    @property
    def is_riichi_furiten(self) -> bool:
        """
        Whether any old discard since the player's riichi discard is
        one of the hand's waits.
        If the player has not called riichi, this will be ``False``.
        """
        if self._riichi_discard_index is None:
            return False
        riichi_back_index = (
            len(self._discard_pool.discards) - 1 - self._riichi_discard_index
        )
        for back_index, discard in enumerate(reversed(self._discard_pool.discards)):
            if back_index == riichi_back_index:
                break
            if discard.is_new:
                continue
            if discard.is_closed_kan:
                continue
            if get_tile_value(discard.tile) in self.waits:
                return True
        return False
