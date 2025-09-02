from pydantic import BaseModel

from .win_info import Yaku, default_yaku_values


class GameOptions(BaseModel):
    player_count: int = 4
    auto_replace_flowers: bool = True
    end_wall_count: int = 14
    game_length: tuple[int, int] = (1, 0)
    start_score: int = 0
    yaku_values: dict[Yaku, int] = default_yaku_values
    score_dealer_win_base_value: int = 3
    score_nondealer_win_base_value: int = 2
    score_dealer_pay_in_base_value: int = 4
