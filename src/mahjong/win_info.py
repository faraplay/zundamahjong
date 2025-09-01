from pydantic import BaseModel

from .tile import Tile
from .call import Call


class WinInfo(BaseModel):
    win_seat: int
    lose_seat: int
    hand: list[Tile]
    calls: list[Call]
