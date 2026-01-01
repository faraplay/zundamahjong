from typing import Any

from zundamahjong.mahjong.call import Call
from zundamahjong.mahjong.meld import Meld
from zundamahjong.mahjong.pattern import get_pattern_mults as gpm
from zundamahjong.mahjong.tile import TileId
from zundamahjong.mahjong.win import Win


def get_pattern_mults(
    *,
    win_player: int = 0,
    lose_player: int | None,
    formed_hand: list[Meld],
    calls: list[Call],
    flowers: list[TileId],
    player_count: int = 4,
    wind_round: int = 0,
    sub_round: int = 0,
    **kwargs: Any,  # pyright: ignore[reportAny, reportExplicitAny]
) -> dict[str, int]:
    hand = [tile for meld in formed_hand for tile in meld.tiles]
    winning_melds = [
        meld for meld in formed_hand if meld.winning_tile_index is not None
    ]
    assert len(winning_melds) == 1
    winning_meld = winning_melds[0]
    assert winning_meld.winning_tile_index is not None
    winning_tile = winning_meld.tiles[winning_meld.winning_tile_index]
    hand.remove(winning_tile)
    hand.append(winning_tile)
    win = Win(
        win_player=win_player,
        lose_player=lose_player,
        hand=hand,
        calls=calls,
        flowers=flowers,
        player_count=player_count,
        wind_round=wind_round,
        sub_round=sub_round,
        **kwargs,  # pyright: ignore[reportAny]
    )
    return gpm(win, formed_hand)
