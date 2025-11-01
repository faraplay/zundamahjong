from pydantic import BaseModel

from .pattern import PatternData, default_pattern_data


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

    calculate_fu: bool = False
    base_fu: int = 25
    round_up_fu: bool = False
    round_up_points: bool = False

    pattern_data: dict[str, PatternData] = default_pattern_data

    @property
    def game_length(self) -> tuple[int, int]:
        return (self.game_length_wind_rounds, self.game_length_sub_rounds)
