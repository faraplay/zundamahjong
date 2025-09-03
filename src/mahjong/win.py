from pydantic import BaseModel

from .tile import Tile
from .call import Call


class Win(BaseModel):
    win_seat: int
    lose_seat: int | None
    hand: list[Tile]
    calls: list[Call]
    after_flower_count: int = 0
    after_kan_count: int = 0
