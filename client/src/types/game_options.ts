export type GameOptions = {
  player_count: number;
  game_length_wind_rounds: number;
  game_length_sub_rounds: number;
  auto_replace_flowers: boolean;
  end_wall_count: number;

  show_waits: boolean;
  show_shanten_info: boolean;

  start_score: number;
  score_dealer_ron_base_value: number;
  score_dealer_tsumo_base_value: number;
  score_nondealer_ron_base_value: number;
  score_nondealer_tsumo_nondealer_base_value: number;
  score_nondealer_tsumo_dealer_base_value: number;

  pattern_values: PatternValues;
};

export const patterns: Pattern[] = [
  "BLESSING_OF_HEAVEN",
  "BLESSING_OF_EARTH",
  "LITTLE_THREE_DRAGONS",
  "BIG_THREE_DRAGONS",
  "FOUR_LITTLE_WINDS",
  "FOUR_BIG_WINDS",
  "FOUR_CONCEALED_TRIPLETS",
  "ALL_HONOURS",
  "ALL_GREENS",
  "ALL_TERMINALS",
  "THIRTEEN_ORPHANS",
  "FOUR_QUADS",
  "NINE_GATES",
  "ALL_RUNS",
  "ALL_SIMPLES",
  "PURE_STRAIGHT",
  "ALL_TRIPLETS",
  "HALF_FLUSH",
  "FULL_FLUSH",
  "SEVEN_PAIRS",
  "HALF_OUTSIDE_HAND",
  "FULLY_OUTSIDE_HAND",
  "PURE_DOUBLE_SEQUENCE",
  "TWICE_PURE_DOUBLE_SEQUENCE",
  "MIXED_TRIPLE_SEQUENCE",
  "TRIPLE_TRIPLETS",
  "ALL_TERMINALS_AND_HONOURS",
  "SEAT_WIND",
  "PREVALENT_WIND",
  "NORTH_WIND",
  "WHITE_DRAGON",
  "GREEN_DRAGON",
  "RED_DRAGON",
  "EYES",
  "NO_CALLS",
  "ROBBING_A_KAN",
  "UNDER_THE_SEA",
  "UNDER_THE_RIVER",
  "AFTER_A_FLOWER",
  "AFTER_A_KAN",
  "NO_FLOWERS",
  "SEAT_FLOWER",
  "SET_OF_FLOWERS",
  "FIVE_FLOWERS",
  "SEVEN_FLOWERS",
  "TWO_SETS_OF_FLOWERS",
  "DRAW",
];

export const patternDisplayNames = {
  BLESSING_OF_HEAVEN: "Blessing of Heaven",
  BLESSING_OF_EARTH: "Blessing of Earth",
  LITTLE_THREE_DRAGONS: "Little Three Dragons",
  BIG_THREE_DRAGONS: "Big Three Dragons",
  FOUR_LITTLE_WINDS: "Four Little Winds",
  FOUR_BIG_WINDS: "Four Big Winds",
  FOUR_CONCEALED_TRIPLETS: "Four Concealed Triplets",
  ALL_HONOURS: "All Honours",
  ALL_GREENS: "All Greens",
  ALL_TERMINALS: "All Terminals",
  THIRTEEN_ORPHANS: "Thirteen Orphans",
  FOUR_QUADS: "Four Quads",
  NINE_GATES: "Nine Gates",
  ALL_RUNS: "All Runs",
  ALL_SIMPLES: "All Simples",
  PURE_STRAIGHT: "Pure Straight",
  ALL_TRIPLETS: "All Triplets",
  HALF_FLUSH: "Half Flush",
  FULL_FLUSH: "Full Flush",
  SEVEN_PAIRS: "Seven Pairs",
  HALF_OUTSIDE_HAND: "Half Outside Hand",
  FULLY_OUTSIDE_HAND: "Fully Outside Hand",
  PURE_DOUBLE_SEQUENCE: "Pure Double Sequence",
  TWICE_PURE_DOUBLE_SEQUENCE: "Twice Pure Double Sequence",
  MIXED_TRIPLE_SEQUENCE: "Mixed Triple Sequence",
  TRIPLE_TRIPLETS: "Triple Triplets",
  ALL_TERMINALS_AND_HONOURS: "All Terminals and Honours",
  SEAT_WIND: "Seat Wind",
  PREVALENT_WIND: "Prevalent Wind",
  NORTH_WIND: "North Wind",
  WHITE_DRAGON: "White Dragon",
  GREEN_DRAGON: "Green Dragon",
  RED_DRAGON: "Red Dragon",
  EYES: "Eyes",
  NO_CALLS: "No Calls",
  ROBBING_A_KAN: "Robbing a Kan",
  UNDER_THE_SEA: "Under the Sea",
  UNDER_THE_RIVER: "Under the River",
  AFTER_A_FLOWER: "After a Flower",
  AFTER_A_KAN: "After a Kan",
  NO_FLOWERS: "No Flowers",
  SEAT_FLOWER: "Seat Flower",
  SET_OF_FLOWERS: "Set of Flowers",
  FIVE_FLOWERS: "Five Flowers",
  SEVEN_FLOWERS: "Seven Flowers",
  TWO_SETS_OF_FLOWERS: "Two Sets of Flowers",
  DRAW: "Draw",
} as const;

export type Pattern = keyof typeof patternDisplayNames;

export type PatternValues = {
  [pattern in Pattern]: number;
};
