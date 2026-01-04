from pydantic import BaseModel

from .call import Call
from .tile import TileId


class Win(BaseModel):
    """
    Holds data associated to a winning hand in a round of mahjong.
    Does not contain the hand's melds or scoring data.
    """

    win_player: int
    "The index of the winning player."
    lose_player: int | None
    "The index of the player who dealt in, or ``None`` if the win was tsumo."
    hand: list[TileId]
    """
    A list of the :py:class:`TileId` s of the tiles in the hand
    (does not include flowers or tiles in calls).
    """
    calls: list[Call]
    "A list of the :py:class:`Call` s that the hand made."
    flowers: list[TileId]

    player_count: int
    "The number of players playing the round of mahjong."
    wind_round: int
    "The wind round number."
    sub_round: int
    "The round number within this wind round."
    draw_count: int = 0
    "The number of consecutive draws before this round."
    after_flower_count: int = 0
    "The number of flowers replaced immediately before drawing the winning tile."
    after_kan_count: int = 0
    "The number of kan bonus tiles drawn immediately before drawing the winning tile."
    is_riichi: bool = False
    "Whether the hand was in riichi."
    is_double_riichi: bool = False
    "Whether the hand was put into riichi on the first turn."
    is_ippatsu: bool = False
    "Whether the hand was won immediately after riichi."
    is_chankan: bool = False
    "Whether the winning tile was stolen from another player's kan."
    is_haitei: bool = False
    "Whether the winning tile was the last draw."
    is_houtei: bool = False
    "Whether the winning tile was the last discard."
    is_tenhou: bool = False
    "Whether the win was by the dealer on the first draw."
    is_chiihou: bool = False
    "Whether the win was by a nondealer on the first draw."
