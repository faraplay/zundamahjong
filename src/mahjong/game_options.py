from pydantic import BaseModel

from .yaku import default_yaku_han


class GameOptions(BaseModel):
    player_count: int = 4
    auto_replace_flowers: bool = True
    end_wall_count: int = 14
    game_length: tuple[int, int] = (1, 0)
    start_score: float = 0.0
    yaku_values: dict[str, int] = default_yaku_han
    score_dealer_ron_base_value: float = 1.5
    score_dealer_tsumo_base_value: float = 1.5
    score_nondealer_ron_base_value: float = 1.0
    score_nondealer_tsumo_nondealer_base_value: float = 0.5
    score_nondealer_tsumo_dealer_base_value: float = 1.0
