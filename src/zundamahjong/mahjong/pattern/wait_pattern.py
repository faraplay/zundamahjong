from enum import IntEnum

from ..meld import MeldType, TileValueMeld


class WaitPattern(IntEnum):
    """
    Enum representing the wait pattern of a winning hand. This is determined by
    how the winning tile fits into its meld.
    """

    RYANMEN = 0
    """
    The winning tile is on one end of a sequence, and the other end of the
    sequence is not a 1 or 9.
    """
    KANCHAN = 1
    """
    The winning tile is in the middle of a sequence.
    """
    PENCHAN = 2
    """
    The winning tile is on one end of a sequence, and the other end of the
    sequence is a 1 or 9.
    """
    SHANPON = 3
    """
    The winning tile is part of a triplet.
    """
    TANKI = 4
    """
    The winning tile is part of a pair.
    """
    KOKUSHI = 5
    """
    The hand is 13 orphans, and the winning tile appears in the hand once.
    """
    KOKUSHI_13 = 6
    """
    The hand is 13 orphans, and the winning tile appears in the hand twice.
    """


def get_wait_pattern(meld: TileValueMeld) -> WaitPattern:
    assert meld.winning_tile_index is not None
    meld_type = meld.meld_type
    if meld_type == MeldType.CHI:
        if meld.winning_tile_index == 0:
            if meld.tiles[0] % 10 == 7:
                return WaitPattern.PENCHAN
            else:
                return WaitPattern.RYANMEN
        elif meld.winning_tile_index == 1:
            return WaitPattern.KANCHAN
        elif meld.winning_tile_index == 2:
            if meld.tiles[2] % 10 == 3:
                return WaitPattern.PENCHAN
            else:
                return WaitPattern.RYANMEN
        else:
            raise Exception(
                f"Unexpected winning tile index {meld.winning_tile_index} in chi meld!"
            )
    elif meld_type == MeldType.PON:
        return WaitPattern.SHANPON
    elif meld_type == MeldType.PAIR:
        return WaitPattern.TANKI
    elif meld_type == MeldType.THIRTEEN_ORPHANS:
        if meld.tiles.count(meld.tiles[meld.winning_tile_index]) == 2:
            return WaitPattern.KOKUSHI_13
        else:
            return WaitPattern.KOKUSHI
    elif meld_type == MeldType.KAN:
        raise Exception("Winning tile found in kan meld!")
    else:
        raise Exception("Unknown meld type!")
