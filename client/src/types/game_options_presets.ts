import type { GameOptions } from "./game_options";

const default_pattern_data = {
  BLESSING_OF_HEAVEN: {
    display_name: "Blessing of Heaven",
    han: 20,
    fu: 0,
  },
  BLESSING_OF_EARTH: {
    display_name: "Blessing of Earth",
    han: 19,
    fu: 0,
  },
  LITTLE_THREE_DRAGONS: {
    display_name: "Little Three Dragons",
    han: 5,
    fu: 0,
  },
  BIG_THREE_DRAGONS: {
    display_name: "Big Three Dragons",
    han: 8,
    fu: 0,
  },
  FOUR_LITTLE_WINDS: {
    display_name: "Four Little Winds",
    han: 12,
    fu: 0,
  },
  FOUR_BIG_WINDS: {
    display_name: "Four Big Winds",
    han: 16,
    fu: 0,
  },
  FOUR_CONCEALED_TRIPLETS: {
    display_name: "Four Concealed Triplets",
    han: 12,
    fu: 0,
  },
  FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT: {
    display_name: "Four Concealed Triplets 1-sided Wait",
    han: 12,
    fu: 0,
  },
  ALL_HONOURS: {
    display_name: "All Honours",
    han: 10,
    fu: 0,
  },
  ALL_GREENS: {
    display_name: "All Greens",
    han: 16,
    fu: 0,
  },
  ALL_TERMINALS: {
    display_name: "All Terminals",
    han: 13,
    fu: 0,
  },
  THIRTEEN_ORPHANS: {
    display_name: "Thirteen Orphans",
    han: 13,
    fu: 0,
  },
  THIRTEEN_ORPHANS_13_SIDED_WAIT: {
    display_name: "Thirteen Orphans 13-sided Wait",
    han: 13,
    fu: 0,
  },
  FOUR_QUADS: {
    display_name: "Four Quads",
    han: 18,
    fu: 0,
  },
  NINE_GATES: {
    display_name: "Nine Gates",
    han: 11,
    fu: 0,
  },
  TRUE_NINE_GATES: {
    display_name: "True Nine Gates",
    han: 19,
    fu: 0,
  },
  ALL_RUNS: {
    display_name: "All Runs",
    han: 1,
    fu: 0,
  },
  ALL_SIMPLES: {
    display_name: "All Simples",
    han: 1,
    fu: 0,
  },
  PURE_STRAIGHT: {
    display_name: "Pure Straight",
    han: 3,
    fu: 0,
  },
  ALL_TRIPLETS: {
    display_name: "All Triplets",
    han: 3,
    fu: 0,
  },
  HALF_FLUSH: {
    display_name: "Half Flush",
    han: 3,
    fu: 0,
  },
  FULL_FLUSH: {
    display_name: "Full Flush",
    han: 7,
    fu: 0,
  },
  SEVEN_PAIRS: {
    display_name: "Seven Pairs",
    han: 3,
    fu: 0,
  },
  HALF_OUTSIDE_HAND: {
    display_name: "Half Outside Hand",
    han: 2,
    fu: 0,
  },
  FULLY_OUTSIDE_HAND: {
    display_name: "Fully Outside Hand",
    han: 4,
    fu: 0,
  },
  PURE_DOUBLE_SEQUENCE: {
    display_name: "Pure Double Sequence",
    han: 1,
    fu: 0,
  },
  TWICE_PURE_DOUBLE_SEQUENCE: {
    display_name: "Twice Pure Double Sequence",
    han: 4,
    fu: 0,
  },
  PURE_TRIPLE_SEQUENCE: {
    display_name: "Pure Triple Sequence",
    han: 6,
    fu: 0,
  },
  PURE_QUADRUPLE_SEQUENCE: {
    display_name: "Pure Quadruple Sequence",
    han: 12,
    fu: 0,
  },
  MIXED_TRIPLE_SEQUENCE: {
    display_name: "Mixed Triple Sequence",
    han: 2,
    fu: 0,
  },
  THREE_CONCEALED_TRIPLETS: {
    display_name: "Three Concealed Triplets",
    han: 3,
    fu: 0,
  },
  THREE_QUADS: {
    display_name: "Three Quads",
    han: 4,
    fu: 0,
  },
  TRIPLE_TRIPLETS: {
    display_name: "Triple Triplets",
    han: 4,
    fu: 0,
  },
  ALL_TERMINALS_AND_HONOURS: {
    display_name: "All Terminals and Honours",
    han: 3,
    fu: 0,
  },
  SEAT_WIND: {
    display_name: "Seat Wind",
    han: 1,
    fu: 0,
  },
  PREVALENT_WIND: {
    display_name: "Prevalent Wind",
    han: 1,
    fu: 0,
  },
  NORTH_WIND: {
    display_name: "North Wind",
    han: 1,
    fu: 0,
  },
  WHITE_DRAGON: {
    display_name: "White Dragon",
    han: 1,
    fu: 0,
  },
  GREEN_DRAGON: {
    display_name: "Green Dragon",
    han: 1,
    fu: 0,
  },
  RED_DRAGON: {
    display_name: "Red Dragon",
    han: 1,
    fu: 0,
  },
  EYES: {
    display_name: "Eyes",
    han: 1,
    fu: 0,
  },
  NO_CALLS: {
    display_name: "No Calls",
    han: 1,
    fu: 0,
  },
  NO_CALLS_TSUMO: {
    display_name: "No Calls Tsumo",
    han: 0,
    fu: 0,
  },
  ROBBING_A_KAN: {
    display_name: "Robbing a Kan",
    han: 1,
    fu: 0,
  },
  UNDER_THE_SEA: {
    display_name: "Under the Sea",
    han: 1,
    fu: 0,
  },
  UNDER_THE_RIVER: {
    display_name: "Under the River",
    han: 1,
    fu: 0,
  },
  AFTER_A_FLOWER: {
    display_name: "After a Flower",
    han: 1,
    fu: 0,
  },
  AFTER_A_KAN: {
    display_name: "After a Kan",
    han: 2,
    fu: 0,
  },
  NO_FLOWERS: {
    display_name: "No Flowers",
    han: 1,
    fu: 0,
  },
  SEAT_FLOWER: {
    display_name: "Seat Flower",
    han: 1,
    fu: 0,
  },
  SET_OF_FLOWERS: {
    display_name: "Set of Flowers",
    han: 2,
    fu: 0,
  },
  FIVE_FLOWERS: {
    display_name: "Five Flowers",
    han: 2,
    fu: 0,
  },
  SEVEN_FLOWERS: {
    display_name: "Seven Flowers",
    han: 2,
    fu: 0,
  },
  TWO_SETS_OF_FLOWERS: {
    display_name: "Two Sets of Flowers",
    han: 8,
    fu: 0,
  },
  DRAW: {
    display_name: "Draw",
    han: 1,
    fu: 0,
  },
  OPEN_WAIT: {
    display_name: "Open Wait",
    han: 0,
    fu: 0,
  },
  CLOSED_WAIT: {
    display_name: "Closed Wait",
    han: 0,
    fu: 2,
  },
  EDGE_WAIT: {
    display_name: "Edge Wait",
    han: 0,
    fu: 2,
  },
  DUAL_PON_WAIT: {
    display_name: "Dual Pon Wait",
    han: 0,
    fu: 0,
  },
  PAIR_WAIT: {
    display_name: "Pair Wait",
    han: 0,
    fu: 2,
  },
  SIMPLE_OPEN_TRIPLET: {
    display_name: "Simple Open Triplet",
    han: 0,
    fu: 2,
  },
  ORPHAN_OPEN_TRIPLET: {
    display_name: "Orphan Open Triplet",
    han: 0,
    fu: 4,
  },
  SIMPLE_CLOSED_TRIPLET: {
    display_name: "Simple Closed Triplet",
    han: 0,
    fu: 4,
  },
  ORPHAN_CLOSED_TRIPLET: {
    display_name: "Orphan Closed Triplet",
    han: 0,
    fu: 8,
  },
  SIMPLE_OPEN_QUAD: {
    display_name: "Simple Open Quad",
    han: 0,
    fu: 8,
  },
  ORPHAN_OPEN_QUAD: {
    display_name: "Orphan Open Quad",
    han: 0,
    fu: 16,
  },
  SIMPLE_CLOSED_QUAD: {
    display_name: "Simple Closed Quad",
    han: 0,
    fu: 16,
  },
  ORPHAN_CLOSED_QUAD: {
    display_name: "Orphan Closed Quad",
    han: 0,
    fu: 32,
  },
  YAKUHAI_PAIR: {
    display_name: "Yakuhai Pair",
    han: 0,
    fu: 2,
  },
  PINFU: {
    display_name: "Pinfu",
    han: 0,
    fu: 0,
  },
  OPEN_PINFU: {
    display_name: "Open Pinfu",
    han: 0,
    fu: 2,
  },
  NO_CALLS_RON: {
    display_name: "No Calls Ron",
    han: 0,
    fu: 10,
  },
  NON_PINFU_TSUMO: {
    display_name: "Non Pinfu Tsumo",
    han: 0,
    fu: 2,
  },
};

export const default_4player_preset: GameOptions = {
  player_count: 4,
  game_length_wind_rounds: 1,
  game_length_sub_rounds: 0,
  auto_replace_flowers: true,
  end_wall_count: 14,
  min_han: 0,
  allow_riichi: false,
  show_waits: true,
  show_shanten_info: false,
  start_score: 0,
  score_dealer_ron_multiplier: 6,
  score_dealer_tsumo_multiplier: 2,
  score_nondealer_ron_multiplier: 4,
  score_nondealer_tsumo_nondealer_multiplier: 1,
  score_nondealer_tsumo_dealer_multiplier: 2,
  calculate_fu: false,
  base_fu: 25,
  round_up_fu: false,
  round_up_points: false,
  pattern_data: default_pattern_data,
};

export const default_3player_preset: GameOptions = {
  player_count: 3,
  game_length_wind_rounds: 1,
  game_length_sub_rounds: 0,
  auto_replace_flowers: true,
  end_wall_count: 14,
  min_han: 0,
  allow_riichi: false,
  show_waits: true,
  show_shanten_info: false,
  start_score: 0,
  score_dealer_ron_multiplier: 6,
  score_dealer_tsumo_multiplier: 3,
  score_nondealer_ron_multiplier: 4,
  score_nondealer_tsumo_nondealer_multiplier: 1.5,
  score_nondealer_tsumo_dealer_multiplier: 2.5,
  calculate_fu: false,
  base_fu: 25,
  round_up_fu: false,
  round_up_points: false,
  pattern_data: default_pattern_data,
};

const riichi_pattern_data = {
  BLESSING_OF_HEAVEN: {
    display_name: "Blessing of Heaven",
    han: 13,
    fu: 0,
  },
  BLESSING_OF_EARTH: {
    display_name: "Blessing of Earth",
    han: 13,
    fu: 0,
  },
  LITTLE_THREE_DRAGONS: {
    display_name: "Little Three Dragons",
    han: 2,
    fu: 0,
  },
  BIG_THREE_DRAGONS: {
    display_name: "Big Three Dragons",
    han: 13,
    fu: 0,
  },
  FOUR_LITTLE_WINDS: {
    display_name: "Four Little Winds",
    han: 13,
    fu: 0,
  },
  FOUR_BIG_WINDS: {
    display_name: "Four Big Winds",
    han: 13,
    fu: 0,
  },
  FOUR_CONCEALED_TRIPLETS: {
    display_name: "Four Concealed Triplets",
    han: 13,
    fu: 0,
  },
  FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT: {
    display_name: "Four Concealed Triplets 1-sided Wait",
    han: 13,
    fu: 0,
  },
  ALL_HONOURS: {
    display_name: "All Honours",
    han: 13,
    fu: 0,
  },
  ALL_GREENS: {
    display_name: "All Greens",
    han: 13,
    fu: 0,
  },
  ALL_TERMINALS: {
    display_name: "All Terminals",
    han: 13,
    fu: 0,
  },
  THIRTEEN_ORPHANS: {
    display_name: "Thirteen Orphans",
    han: 13,
    fu: 0,
  },
  THIRTEEN_ORPHANS_13_SIDED_WAIT: {
    display_name: "Thirteen Orphans 13-sided Wait",
    han: 13,
    fu: 0,
  },
  FOUR_QUADS: {
    display_name: "Four Quads",
    han: 13,
    fu: 0,
  },
  NINE_GATES: {
    display_name: "Nine Gates",
    han: 13,
    fu: 0,
  },
  TRUE_NINE_GATES: {
    display_name: "True Nine Gates",
    han: 13,
    fu: 0,
  },
  ALL_RUNS: {
    display_name: "All Runs",
    han: 0,
    fu: 0,
  },
  ALL_SIMPLES: {
    display_name: "All Simples",
    han: 1,
    fu: 0,
  },
  PURE_STRAIGHT: {
    display_name: "Pure Straight",
    han: 2,
    fu: 0,
  },
  ALL_TRIPLETS: {
    display_name: "All Triplets",
    han: 2,
    fu: 0,
  },
  HALF_FLUSH: {
    display_name: "Half Flush",
    han: 3,
    fu: 0,
  },
  FULL_FLUSH: {
    display_name: "Full Flush",
    han: 6,
    fu: 0,
  },
  SEVEN_PAIRS: {
    display_name: "Seven Pairs",
    han: 2,
    fu: 0,
  },
  HALF_OUTSIDE_HAND: {
    display_name: "Half Outside Hand",
    han: 2,
    fu: 0,
  },
  FULLY_OUTSIDE_HAND: {
    display_name: "Fully Outside Hand",
    han: 3,
    fu: 0,
  },
  PURE_DOUBLE_SEQUENCE: {
    display_name: "Pure Double Sequence",
    han: 1,
    fu: 0,
  },
  TWICE_PURE_DOUBLE_SEQUENCE: {
    display_name: "Twice Pure Double Sequence",
    han: 3,
    fu: 0,
  },
  PURE_TRIPLE_SEQUENCE: {
    display_name: "Pure Triple Sequence",
    han: 1,
    fu: 0,
  },
  PURE_QUADRUPLE_SEQUENCE: {
    display_name: "Pure Quadruple Sequence",
    han: 3,
    fu: 0,
  },
  MIXED_TRIPLE_SEQUENCE: {
    display_name: "Mixed Triple Sequence",
    han: 2,
    fu: 0,
  },
  THREE_CONCEALED_TRIPLETS: {
    display_name: "Three Concealed Triplets",
    han: 2,
    fu: 0,
  },
  THREE_QUADS: {
    display_name: "Three Quads",
    han: 2,
    fu: 0,
  },
  TRIPLE_TRIPLETS: {
    display_name: "Triple Triplets",
    han: 2,
    fu: 0,
  },
  ALL_TERMINALS_AND_HONOURS: {
    display_name: "All Terminals and Honours",
    han: 0,
    fu: 0,
  },
  SEAT_WIND: {
    display_name: "Seat Wind",
    han: 1,
    fu: 0,
  },
  PREVALENT_WIND: {
    display_name: "Prevalent Wind",
    han: 1,
    fu: 0,
  },
  NORTH_WIND: {
    display_name: "North Wind",
    han: 1,
    fu: 0,
  },
  WHITE_DRAGON: {
    display_name: "White Dragon",
    han: 1,
    fu: 0,
  },
  GREEN_DRAGON: {
    display_name: "Green Dragon",
    han: 1,
    fu: 0,
  },
  RED_DRAGON: {
    display_name: "Red Dragon",
    han: 1,
    fu: 0,
  },
  EYES: {
    display_name: "Eyes",
    han: 0,
    fu: 0,
  },
  NO_CALLS: {
    display_name: "No Calls",
    han: 0,
    fu: 0,
  },
  NO_CALLS_TSUMO: {
    display_name: "No Calls Tsumo",
    han: 1,
    fu: 0,
  },
  ROBBING_A_KAN: {
    display_name: "Robbing a Kan",
    han: 1,
    fu: 0,
  },
  UNDER_THE_SEA: {
    display_name: "Under the Sea",
    han: 1,
    fu: 0,
  },
  UNDER_THE_RIVER: {
    display_name: "Under the River",
    han: 1,
    fu: 0,
  },
  AFTER_A_FLOWER: {
    display_name: "After a Flower",
    han: 1,
    fu: 0,
  },
  AFTER_A_KAN: {
    display_name: "After a Kan",
    han: 1,
    fu: 0,
  },
  NO_FLOWERS: {
    display_name: "No Flowers",
    han: 1,
    fu: 0,
  },
  SEAT_FLOWER: {
    display_name: "Seat Flower",
    han: 1,
    fu: 0,
  },
  SET_OF_FLOWERS: {
    display_name: "Set of Flowers",
    han: 2,
    fu: 0,
  },
  FIVE_FLOWERS: {
    display_name: "Five Flowers",
    han: 2,
    fu: 0,
  },
  SEVEN_FLOWERS: {
    display_name: "Seven Flowers",
    han: 2,
    fu: 0,
  },
  TWO_SETS_OF_FLOWERS: {
    display_name: "Two Sets of Flowers",
    han: 8,
    fu: 0,
  },
  DRAW: {
    display_name: "Draw",
    han: 0,
    fu: 0,
  },
  OPEN_WAIT: {
    display_name: "Open Wait",
    han: 0,
    fu: 0,
  },
  CLOSED_WAIT: {
    display_name: "Closed Wait",
    han: 0,
    fu: 2,
  },
  EDGE_WAIT: {
    display_name: "Edge Wait",
    han: 0,
    fu: 2,
  },
  DUAL_PON_WAIT: {
    display_name: "Dual Pon Wait",
    han: 0,
    fu: 0,
  },
  PAIR_WAIT: {
    display_name: "Pair Wait",
    han: 0,
    fu: 2,
  },
  SIMPLE_OPEN_TRIPLET: {
    display_name: "Simple Open Triplet",
    han: 0,
    fu: 2,
  },
  ORPHAN_OPEN_TRIPLET: {
    display_name: "Orphan Open Triplet",
    han: 0,
    fu: 4,
  },
  SIMPLE_CLOSED_TRIPLET: {
    display_name: "Simple Closed Triplet",
    han: 0,
    fu: 4,
  },
  ORPHAN_CLOSED_TRIPLET: {
    display_name: "Orphan Closed Triplet",
    han: 0,
    fu: 8,
  },
  SIMPLE_OPEN_QUAD: {
    display_name: "Simple Open Quad",
    han: 0,
    fu: 8,
  },
  ORPHAN_OPEN_QUAD: {
    display_name: "Orphan Open Quad",
    han: 0,
    fu: 16,
  },
  SIMPLE_CLOSED_QUAD: {
    display_name: "Simple Closed Quad",
    han: 0,
    fu: 16,
  },
  ORPHAN_CLOSED_QUAD: {
    display_name: "Orphan Closed Quad",
    han: 0,
    fu: 32,
  },
  YAKUHAI_PAIR: {
    display_name: "Yakuhai Pair",
    han: 0,
    fu: 2,
  },
  PINFU: {
    display_name: "Pinfu",
    han: 1,
    fu: 0,
  },
  OPEN_PINFU: {
    display_name: "Open Pinfu",
    han: 0,
    fu: 2,
  },
  NO_CALLS_RON: {
    display_name: "No Calls Ron",
    han: 0,
    fu: 10,
  },
  NON_PINFU_TSUMO: {
    display_name: "Non Pinfu Tsumo",
    han: 0,
    fu: 2,
  },
};

export const riichi_4player_preset: GameOptions = {
  player_count: 4,
  game_length_wind_rounds: 1,
  game_length_sub_rounds: 0,
  auto_replace_flowers: true,
  end_wall_count: 14,
  min_han: 1,
  allow_riichi: true,
  show_waits: true,
  start_score: 25000,
  score_dealer_ron_multiplier: 6,
  score_dealer_tsumo_multiplier: 2,
  score_nondealer_ron_multiplier: 4,
  score_nondealer_tsumo_nondealer_multiplier: 1,
  score_nondealer_tsumo_dealer_multiplier: 2,
  calculate_fu: true,
  base_fu: 20,
  round_up_fu: true,
  round_up_points: true,
  show_shanten_info: false,
  pattern_data: riichi_pattern_data,
};

export const riichi_3player_preset: GameOptions = {
  player_count: 3,
  game_length_wind_rounds: 1,
  game_length_sub_rounds: 0,
  auto_replace_flowers: true,
  end_wall_count: 14,
  min_han: 1,
  allow_riichi: true,
  show_waits: true,
  start_score: 35000,
  score_dealer_ron_multiplier: 6,
  score_dealer_tsumo_multiplier: 3,
  score_nondealer_ron_multiplier: 4,
  score_nondealer_tsumo_nondealer_multiplier: 1.5,
  score_nondealer_tsumo_dealer_multiplier: 2.5,
  calculate_fu: true,
  base_fu: 20,
  round_up_fu: true,
  round_up_points: true,
  show_shanten_info: false,
  pattern_data: riichi_pattern_data,
};
