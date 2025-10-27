from pydantic import BaseModel

from .call import Call
from .tile import TileId


class Win(BaseModel):
    win_player: int
    lose_player: int | None
    hand: list[TileId]
    calls: list[Call]
    flowers: list[TileId]

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
