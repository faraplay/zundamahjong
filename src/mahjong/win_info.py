from typing import NamedTuple

from .tile import Tile
from .call import Call


class WinInfo(NamedTuple):
    win_seat: int
    lose_seat: int
    hand: list[Tile]
    calls: list[Call]
