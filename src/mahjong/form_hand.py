from collections.abc import Sequence

from .tile import Tile, orphans
from .call import Call, CallType


def is_winning(tiles: Sequence[Tile]):
    return len(formed_hand_possibilities(tiles)) > 0


def formed_hand_possibilities(tiles: Sequence[Tile]):
    formed_hands = standard_formed_hand_possibilities(tiles)
    if len(tiles) == 14:
        formed_hands.extend(form_seven_pairs(tiles))
        formed_hands.extend(form_thirteen_orphans(tiles))
    return formed_hands


def standard_formed_hand_possibilities(tiles: Sequence[Tile]):
    if len(tiles) % 3 != 2:
        return []
    suits: list[list[Tile]] = [[] for _ in range(4)]
    for tile in sorted(tiles):
        if tile < 10:
            suits[0].append(tile)
        elif tile < 20:
            suits[1].append(tile)
        elif tile < 30:
            suits[2].append(tile)
        else:
            suits[3].append(tile)
    if sum(len(suit) % 3 != 0 for suit in suits) != 1:
        return []
    formed_hands: list[list[Call]] = [[]]
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


def split_suit_into_pons(tiles: Sequence[Tile]) -> list[list[Call]]:
    assert len(tiles) % 3 == 0
    tile_counts = dict((tile, tiles.count(tile)) for tile in set(tiles))
    assert all(count <= 4 for count in tile_counts.values())
    if all(count == 3 for count in tile_counts.values()):
        return [
            [
                Call(call_type=CallType.PON, tiles=[tile, tile, tile])
                for tile in tile_counts.keys()
            ]
        ]
    else:
        return []


def split_suit_into_pons_and_pair(tiles: Sequence[Tile]) -> list[list[Call]]:
    assert len(tiles) % 3 == 2
    tile_counts = dict((tile, tiles.count(tile)) for tile in set(tiles))
    assert all(count <= 4 for count in tile_counts.values())
    if sum(count != 3 for count in tile_counts.values()) == 1:
        return [
            [
                (
                    Call(call_type=CallType.PON, tiles=[tile, tile, tile])
                    if count == 3
                    else Call(call_type=CallType.PAIR, tiles=[tile, tile])
                )
                for (tile, count) in tile_counts.items()
            ]
        ]
    else:
        return []


def split_suit_into_3melds(tiles: Sequence[Tile]) -> list[list[Call]]:
    assert len(tiles) % 3 == 0
    assert tiles == sorted(tiles)
    if len(tiles) == 0:
        return [[]]
    tiles = list(tiles)
    tile = tiles[0]
    formed_hands: list[list[Call]] = []
    if tiles[2] == tile:
        remaining_tiles = tiles[3:]
        formed_hands.extend(
            [Call(call_type=CallType.PON, tiles=[tile, tile, tile])] + formed_hand
            for formed_hand in split_suit_into_3melds(remaining_tiles)
        )
    try:
        remaining_tiles = tiles[1:]
        remaining_tiles.remove(tile + 1)
        remaining_tiles.remove(tile + 2)
        formed_hands.extend(
            [Call(call_type=CallType.CHI, tiles=[tile, tile + 1, tile + 2])]
            + formed_hand
            for formed_hand in split_suit_into_3melds(remaining_tiles)
        )
    except ValueError:
        pass
    return formed_hands


def split_suit_into_3melds_and_pair(tiles: Sequence[Tile]) -> list[list[Call]]:
    assert len(tiles) % 3 == 2
    assert tiles == sorted(tiles)
    tile_sum = sum(tiles)
    formed_hands: list[list[Call]] = []
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
            [Call(call_type=CallType.PAIR, tiles=[tile, tile])] + formed_hand
            for formed_hand in split_suit_into_3melds(remaining_tiles)
        )
    return formed_hands


def form_seven_pairs(tiles: Sequence[Tile]) -> list[list[Call]]:
    assert len(tiles) == 14
    tile_counts = dict((tile, tiles.count(tile)) for tile in set(tiles))
    if all(count == 2 for count in tile_counts.values()):
        return [
            [
                Call(call_type=CallType.PAIR, tiles=[tile, tile])
                for tile in tile_counts.keys()
            ]
        ]
    else:
        return []


def form_thirteen_orphans(tiles: Sequence[Tile]) -> list[list[Call]]:
    assert len(tiles) == 14
    tiles_list = list(tiles)
    try:
        for tile in orphans:
            tiles_list.remove(tile)
        assert len(tiles_list) == 1
        if tiles_list[0] in orphans:
            return [
                [Call(call_type=CallType.THIRTEEN_ORPHANS, tiles=list(tiles).sort())]
            ]
        else:
            return []
    except ValueError:
        return []
