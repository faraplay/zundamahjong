from collections.abc import Sequence

from .tile import TileId, TileValue, get_tile_values, orphans, remove_tile_value
from .meld import MeldType, Meld, TileValueMeld


def is_winning(tiles: list[TileId]) -> bool:
    return len(formed_hand_possibilities(tiles)) > 0


def formed_hand_possibilities(tiles: list[TileId]) -> list[list[Meld]]:
    formed_hands = standard_formed_hand_possibilities(tiles)
    if len(tiles) == 14:
        formed_hands.extend(form_seven_pairs(tiles))
        formed_hands.extend(form_thirteen_orphans(tiles))
    return [reconstruct_formed_hand(tiles, formed_hand) for formed_hand in formed_hands]


def reconstruct_formed_hand(
    tiles: Sequence[TileId], tile_value_melds: list[TileValueMeld]
) -> list[Meld]:
    tiles_copy = list(tiles)
    return [
        Meld(
            meld_type=tile_value_meld.meld_type,
            tiles=[
                remove_tile_value(tiles_copy, tile_value)
                for tile_value in tile_value_meld.tiles
            ],
        )
        for tile_value_meld in tile_value_melds
    ]


def standard_formed_hand_possibilities(
    tiles: list[TileId],
) -> list[list[TileValueMeld]]:
    tile_values = get_tile_values(tiles)
    if len(tile_values) % 3 != 2:
        return []
    suits: list[list[TileValue]] = [[] for _ in range(4)]
    for tile_value in sorted(tile_values):
        if tile_value < 10:
            suits[0].append(tile_value)
        elif tile_value < 20:
            suits[1].append(tile_value)
        elif tile_value < 30:
            suits[2].append(tile_value)
        else:
            suits[3].append(tile_value)
    if sum(len(suit) % 3 != 0 for suit in suits) != 1:
        return []
    formed_hands: list[list[TileValueMeld]] = [[]]
    for index, suit in enumerate(suits):
        if len(formed_hands) == 0:
            return formed_hands
        if index < 3:
            if len(suit) % 3 == 2:
                suit_formed_hands = split_suit_into_3melds_and_pair(suit)
            else:
                suit_formed_hands = split_suit_into_3melds(suit)
        else:
            if len(suit) % 3 == 2:
                suit_formed_hands = split_suit_into_pons_and_pair(suit)
            else:
                suit_formed_hands = split_suit_into_pons(suit)
        formed_hands = [
            formed_hand + suit_formed_hand
            for formed_hand in formed_hands
            for suit_formed_hand in suit_formed_hands
        ]
    return formed_hands


def split_suit_into_pons(tiles: list[TileValue]) -> list[list[TileValueMeld]]:
    assert len(tiles) % 3 == 0
    tile_counts = dict((tile, tiles.count(tile)) for tile in set(tiles))
    assert all(count <= 4 for count in tile_counts.values())
    if all(count == 3 for count in tile_counts.values()):
        return [
            [
                TileValueMeld(meld_type=MeldType.PON, tiles=[tile, tile, tile])
                for tile in tile_counts.keys()
            ]
        ]
    else:
        return []


def split_suit_into_pons_and_pair(
    tiles: list[TileValue],
) -> list[list[TileValueMeld]]:
    assert len(tiles) % 3 == 2
    tile_counts = dict((tile, tiles.count(tile)) for tile in set(tiles))
    assert all(count <= 4 for count in tile_counts.values())
    if sum(count != 3 for count in tile_counts.values()) == 1:
        return [
            [
                (
                    TileValueMeld(meld_type=MeldType.PON, tiles=[tile, tile, tile])
                    if count == 3
                    else TileValueMeld(meld_type=MeldType.PAIR, tiles=[tile, tile])
                )
                for (tile, count) in tile_counts.items()
            ]
        ]
    else:
        return []


def split_suit_into_3melds(tiles: list[TileValue]) -> list[list[TileValueMeld]]:
    assert len(tiles) % 3 == 0
    assert tiles == sorted(tiles)
    if len(tiles) == 0:
        return [[]]
    tiles = list(tiles)
    tile = tiles[0]
    formed_hands: list[list[TileValueMeld]] = []
    if tiles[2] == tile:
        remaining_tiles = tiles[3:]
        formed_hands.extend(
            [TileValueMeld(meld_type=MeldType.PON, tiles=[tile, tile, tile])]
            + formed_hand
            for formed_hand in split_suit_into_3melds(remaining_tiles)
        )
    try:
        remaining_tiles = tiles[1:]
        remaining_tiles.remove(tile + 1)
        remaining_tiles.remove(tile + 2)
        formed_hands.extend(
            [TileValueMeld(meld_type=MeldType.CHI, tiles=[tile, tile + 1, tile + 2])]
            + formed_hand
            for formed_hand in split_suit_into_3melds(remaining_tiles)
        )
    except ValueError:
        pass
    return formed_hands


def split_suit_into_3melds_and_pair(
    tiles: list[TileValue],
) -> list[list[TileValueMeld]]:
    assert len(tiles) % 3 == 2
    assert tiles == sorted(tiles)
    tile_sum = sum(tiles)
    formed_hands: list[list[TileValueMeld]] = []
    for index, tile in enumerate(tiles):
        if index > 0 and tiles[index - 1] == tile:
            continue
        if index == len(tiles) - 1:
            continue
        if tiles[index + 1] != tile:
            continue
        if (tile_sum - 2 * tile) % 3 != 0:
            continue
        remaining_tiles = tiles[:index] + tiles[index + 2 :]
        formed_hands.extend(
            [TileValueMeld(meld_type=MeldType.PAIR, tiles=[tile, tile])] + formed_hand
            for formed_hand in split_suit_into_3melds(remaining_tiles)
        )
    return formed_hands


def form_seven_pairs(tiles: list[TileId]) -> list[list[TileValueMeld]]:
    tile_values = get_tile_values(tiles)
    if len(tile_values) != 14:
        return []
    tile_counts = dict((tile, tile_values.count(tile)) for tile in set(tile_values))
    if all(count == 2 for count in tile_counts.values()):
        return [
            [
                TileValueMeld(meld_type=MeldType.PAIR, tiles=[tile, tile])
                for tile in tile_counts.keys()
            ]
        ]
    else:
        return []


def form_thirteen_orphans(tiles: list[TileId]) -> list[list[TileValueMeld]]:
    tile_values = get_tile_values(tiles)
    if len(tile_values) != 14:
        return []
    tiles_list = list(tile_values)
    try:
        for tile in orphans:
            tiles_list.remove(tile)
        assert len(tiles_list) == 1
        if tiles_list[0] in orphans:
            return [
                [
                    TileValueMeld(
                        meld_type=MeldType.THIRTEEN_ORPHANS,
                        tiles=sorted(list(tile_values)),
                    )
                ]
            ]
        else:
            return []
    except ValueError:
        return []
