import type { PatternDataDict } from "./pattern";

export type GameOptions = {
  player_count: number;
  game_length_wind_rounds: number;
  game_length_sub_rounds: number;
  use_flowers: boolean;
  auto_replace_flowers: boolean;
  min_yaku: number;

  allow_riichi: boolean;
  riichi_cost: number;
  can_riichi_negative_score: boolean;

  allow_rob_added_kan: boolean;
  allow_thirteen_orphans_rob_closed_kan: boolean;
  allow_rob_closed_kan: boolean;

  use_temporary_furiten: boolean;
  use_riichi_furiten: boolean;
  use_own_discard_furiten: boolean;

  end_last_round_if_dealer_ahead: boolean;

  show_waits: boolean;
  show_shanten_info: boolean;

  max_kan_count: number;
  max_dora_count: number;
  start_dora_count: number;
  dead_wall_additional_tiles: number;

  start_score: number;
  score_dealer_ron_multiplier: number;
  score_dealer_tsumo_multiplier: number;
  score_nondealer_ron_multiplier: number;
  score_nondealer_tsumo_nondealer_multiplier: number;
  score_nondealer_tsumo_dealer_multiplier: number;

  calculate_fu: boolean;
  base_fu: number;
  round_up_fu: boolean;
  seven_pairs_use_fixed_fu: boolean;
  seven_pairs_fixed_fu: number;
  round_up_points: boolean;

  base_score_limits: ScoreLimit[];

  pattern_data: PatternDataDict;
};

export type ScoreLimit = {
  han: number;
  score: number;
};
