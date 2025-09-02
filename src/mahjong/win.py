from pydantic import BaseModel

from .tile import Tile
from .call import Call


class Win(BaseModel):
    win_seat: int
    lose_seat: int | None
    hand: list[Tile]
    calls: list[Call]
