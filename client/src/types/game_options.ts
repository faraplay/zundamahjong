import type { PatternDataDict } from "./pattern";

export type GameOptions = {
  player_count: number;
  game_length_wind_rounds: number;
  game_length_sub_rounds: number;
  use_flowers: boolean;
  auto_replace_flowers: boolean;
  end_wall_count: number;
  min_han: number;

  allow_riichi: boolean;

  allow_rob_added_kan: boolean;
  allow_thirteen_orphans_rob_closed_kan: boolean;
  allow_rob_closed_kan: boolean;

  use_temporary_furiten: boolean;
  use_riichi_furiten: boolean;
  use_own_discard_furiten: boolean;

  show_waits: boolean;
  show_shanten_info: boolean;

  start_score: number;
  score_dealer_ron_multiplier: number;
  score_dealer_tsumo_multiplier: number;
  score_nondealer_ron_multiplier: number;
  score_nondealer_tsumo_nondealer_multiplier: number;
  score_nondealer_tsumo_dealer_multiplier: number;

  calculate_fu: boolean;
  base_fu: number;
  round_up_fu: boolean;
  round_up_points: boolean;

  base_score_limits: ScoreLimit[];

  pattern_data: PatternDataDict;
};

export type ScoreLimit = {
  han: number;
  score: number;
};
