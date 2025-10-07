from pydantic import BaseModel

from .yaku import default_yaku_han


class GameOptions(BaseModel):
    player_count: int = 4
    game_length_wind_rounds: int = 1
    game_length_sub_rounds: int = 0
    auto_replace_flowers: bool = True
    end_wall_count: int = 14

    show_waits: bool = True
    show_shanten_info: bool = False

    start_score: float = 0.0
    score_dealer_ron_base_value: float = 1.5
    score_dealer_tsumo_base_value: float = 1.0
    score_nondealer_ron_base_value: float = 1.0
    score_nondealer_tsumo_nondealer_base_value: float = 0.5
    score_nondealer_tsumo_dealer_base_value: float = 1.0

    yaku_values: dict[str, int] = default_yaku_han

    @property
    def game_length(self):
        return (self.game_length_wind_rounds, self.game_length_sub_rounds)
