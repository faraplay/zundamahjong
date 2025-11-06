export type GameOptions = {
  player_count: number;
  game_length_wind_rounds: number;
  game_length_sub_rounds: number;
  auto_replace_flowers: boolean;
  end_wall_count: number;

  allow_riichi: boolean;

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

  pattern_data: PatternDataDict;
};

export type PatternData = {
  display_name: string;
  han: number;
  fu: number;
};

export const patterns = [
  "BLESSING_OF_HEAVEN",
  "BLESSING_OF_EARTH",
  "LITTLE_THREE_DRAGONS",
  "BIG_THREE_DRAGONS",
  "FOUR_LITTLE_WINDS",
  "FOUR_BIG_WINDS",
  "FOUR_CONCEALED_TRIPLETS",
  "FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT",
  "ALL_HONOURS",
  "ALL_GREENS",
  "ALL_TERMINALS",
  "THIRTEEN_ORPHANS",
  "THIRTEEN_ORPHANS_13_SIDED_WAIT",
  "FOUR_QUADS",
  "NINE_GATES",
  "TRUE_NINE_GATES",
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
  "PURE_TRIPLE_SEQUENCE",
  "PURE_QUADRUPLE_SEQUENCE",
  "MIXED_TRIPLE_SEQUENCE",
  "THREE_CONCEALED_TRIPLETS",
  "THREE_QUADS",
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
  "NO_CALLS_TSUMO",
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
  "OPEN_WAIT",
  "CLOSED_WAIT",
  "EDGE_WAIT",
  "DUAL_PON_WAIT",
  "PAIR_WAIT",
  "SIMPLE_OPEN_TRIPLET",
  "ORPHAN_OPEN_TRIPLET",
  "SIMPLE_CLOSED_TRIPLET",
  "ORPHAN_CLOSED_TRIPLET",
  "SIMPLE_OPEN_QUAD",
  "ORPHAN_OPEN_QUAD",
  "SIMPLE_CLOSED_QUAD",
  "ORPHAN_CLOSED_QUAD",
  "YAKUHAI_PAIR",
  "PINFU",
  "OPEN_PINFU",
  "NO_CALLS_RON",
  "NON_PINFU_TSUMO",
] as const;

export const patternDisplayNames = {
  BLESSING_OF_HEAVEN: "Blessing of Heaven",
  BLESSING_OF_EARTH: "Blessing of Earth",
  LITTLE_THREE_DRAGONS: "Little Three Dragons",
  BIG_THREE_DRAGONS: "Big Three Dragons",
  FOUR_LITTLE_WINDS: "Four Little Winds",
  FOUR_BIG_WINDS: "Four Big Winds",
  FOUR_CONCEALED_TRIPLETS: "Four Concealed Triplets",
  FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT: "Four Concealed Triplets 1-sided Wait",
  ALL_HONOURS: "All Honours",
  ALL_GREENS: "All Greens",
  ALL_TERMINALS: "All Terminals",
  THIRTEEN_ORPHANS: "Thirteen Orphans",
  THIRTEEN_ORPHANS_13_SIDED_WAIT: "Thirteen Orphans 13-sided Wait",
  FOUR_QUADS: "Four Quads",
  NINE_GATES: "Nine Gates",
  TRUE_NINE_GATES: "True Nine Gates",
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
  PURE_TRIPLE_SEQUENCE: "Pure Triple Sequence",
  PURE_QUADRUPLE_SEQUENCE: "Pure Quadruple Sequence",
  MIXED_TRIPLE_SEQUENCE: "Mixed Triple Sequence",
  THREE_CONCEALED_TRIPLETS: "Three Concealed Triplets",
  THREE_QUADS: "Three Quads",
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
  NO_CALLS_TSUMO: "No Calls Tsumo",
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
  OPEN_WAIT: "Open Wait",
  CLOSED_WAIT: "Closed Wait",
  EDGE_WAIT: "Edge Wait",
  DUAL_PON_WAIT: "Dual Pon Wait",
  PAIR_WAIT: "Pair Wait",
  SIMPLE_OPEN_TRIPLET: "Simple Open Triplet",
  ORPHAN_OPEN_TRIPLET: "Orphan Open Triplet",
  SIMPLE_CLOSED_TRIPLET: "Simple Closed Triplet",
  ORPHAN_CLOSED_TRIPLET: "Orphan Closed Triplet",
  SIMPLE_OPEN_QUAD: "Simple Open Quad",
  ORPHAN_OPEN_QUAD: "Orphan Open Quad",
  SIMPLE_CLOSED_QUAD: "Simple Closed Quad",
  ORPHAN_CLOSED_QUAD: "Orphan Closed Quad",
  YAKUHAI_PAIR: "Yakuhai Pair",
  PINFU: "Pinfu",
  OPEN_PINFU: "Open Pinfu",
  NO_CALLS_RON: "No Calls Ron",
  NON_PINFU_TSUMO: "Non Pinfu Tsumo",
} as const;

export type Pattern = keyof typeof patternDisplayNames;

export type PatternDataDict = {
  [pattern in Pattern]: PatternData;
};
