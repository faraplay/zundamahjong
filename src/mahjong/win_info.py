from typing import NamedTuple

from .tile import Tile
from .call import Call


class WinInfo(NamedTuple):
    win_player: int
    lose_player: int
    hand: list[Tile]
    calls: list[Call]
