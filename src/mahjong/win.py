from pydantic import BaseModel

from .tile import Tile
from .call import Call


class Win(BaseModel):
    win_player: int
    lose_player: int | None
    hand: list[Tile]
    calls: list[Call]
    flowers: list[Tile]

    player_count: int
    wind_round: int
    sub_round: int
    draw_count: int = 0
    after_flower_count: int = 0
    after_kan_count: int = 0
    is_chankan: bool = False
    is_haitei: bool = False
    is_houtei: bool = False
    is_tenhou: bool = False
    is_chiihou: bool = False
