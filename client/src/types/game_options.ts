export type GameOptions = {
  player_count: number;
  auto_replace_flowers: boolean;
  end_wall_count: number;
  game_length_wind_rounds: number;
  game_length_sub_rounds: number;
  start_score: number;
  yaku_values: { [yaku: string]: number };
  score_dealer_ron_base_value: number;
  score_dealer_tsumo_base_value: number;
  score_nondealer_ron_base_value: number;
  score_nondealer_tsumo_nondealer_base_value: number;
  score_nondealer_tsumo_dealer_base_value: number;
};

export const defaultGameOptions: GameOptions = {
  player_count: 4,
  auto_replace_flowers: true,
  end_wall_count: 14,
  game_length_wind_rounds: 1,
  game_length_sub_rounds: 0,
  start_score: 0.0,
  yaku_values: {},
  score_dealer_ron_base_value: 1.5,
  score_dealer_tsumo_base_value: 1.0,
  score_nondealer_ron_base_value: 1.0,
  score_nondealer_tsumo_nondealer_base_value: 0.5,
  score_nondealer_tsumo_dealer_base_value: 1.0,
} as const;
