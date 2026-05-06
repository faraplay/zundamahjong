export type PatternData = {
  display_name: string;
  han: number;
  fu: number;
};

type PatternDesc = {
  displayName: string;
  description: string;
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
  "RIICHI",
  "DOUBLE_RIICHI",
  "IPPATSU",
  "ALL_SEQUENCES",
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
  "CLOSED_PINFU",
  "OPEN_PINFU",
  "NO_CALLS_RON",
  "NON_PINFU_TSUMO",
] as const;

export const patternDescs: {
  [pattern in Pattern]: PatternDesc;
} = {
  BLESSING_OF_HEAVEN: {
    displayName: "Blessing of Heaven",
    description: "(Dealer only) Win on your first draw.",
  },
  BLESSING_OF_EARTH: {
    displayName: "Blessing of Earth",
    description: "(Non-dealer only) Win on your first draw.",
  },
  RIICHI: { displayName: "Riichi", description: "Win after calling riichi." },
  DOUBLE_RIICHI: {
    displayName: "Double Riichi",
    description: "Win after calling riichi on your first turn.",
  },
  IPPATSU: {
    displayName: "Ippatsu",
    description: "Win after calling riichi before you make any more discards.",
  },
  ROBBING_A_KAN: {
    displayName: "Robbing a Kan",
    description:
      "Win from a tile another player is using to form an added or closed kan.",
  },
  UNDER_THE_SEA: {
    displayName: "Under the Sea",
    description: "Win on the final draw.",
  },
  UNDER_THE_RIVER: {
    displayName: "Under the River",
    description: "Win on the final discard.",
  },
  AFTER_A_FLOWER: {
    displayName: "After a Flower",
    description: "Win on the tile drawn after replacing a flower.",
  },
  AFTER_A_KAN: {
    displayName: "After a Kan",
    description: "Win on the tile drawn after calling a kan.",
  },
  DRAW: {
    displayName: "Draw",
    description: "Win after the previous round is a draw.",
  },

  ALL_SEQUENCES: {
    displayName: "All Sequences",
    description: "All four melds are sequences.",
  },
  PURE_DOUBLE_SEQUENCE: {
    displayName: "Pure Double Sequence",
    description: "The hand contains one pair of identical sequences.",
  },
  TWICE_PURE_DOUBLE_SEQUENCE: {
    displayName: "Twice Pure Double Sequence",
    description: "The hand contains two pairs of identical sequences.",
  },
  PURE_TRIPLE_SEQUENCE: {
    displayName: "Pure Triple Sequence",
    description: "The hand contains three identical sequences.",
  },
  PURE_QUADRUPLE_SEQUENCE: {
    displayName: "Pure Quadruple Sequence",
    description: "The hand contains four identical sequences.",
  },
  PURE_STRAIGHT: {
    displayName: "Pure Straight",
    description:
      "The hand contains sequences of 123, 456, 789 in the same suit.",
  },
  MIXED_TRIPLE_SEQUENCE: {
    displayName: "Mixed Triple Sequence",
    description: `
      The hand contains three sequences of the same numbers in different suits.
    `,
  },

  CLOSED_PINFU: {
    displayName: "Pinfu",
    description: `
      All four melds in the hand are sequences, the wait pattern is an open
      wait, the pair is not a yakuhai tile, and the hand is closed.
    `,
  },
  OPEN_PINFU: {
    displayName: "Open Pinfu",
    description: `
      All four melds in the hand are sequences, the wait pattern is an open
      wait, the pair is not a yakuhai tile, and the hand is open.
    `,
  },
  NON_PINFU_TSUMO: {
    displayName: "Non Pinfu Tsumo",
    description: `
      The winning tile was drawn by the player, and the hand does not
      qualify for pinfu.
    `,
  },

  ALL_TRIPLETS: {
    displayName: "All Triplets",
    description: "All four melds in the hand are triplets or quads.",
  },
  TRIPLE_TRIPLETS: {
    displayName: "Triple Triplets",
    description: `
      The hand has three triplets or quads of the same number in different
      suits.
    `,
  },
  THREE_CONCEALED_TRIPLETS: {
    displayName: "Three Concealed Triplets",
    description: `
      The hand contains three closed triplets or quads.
    `,
  },
  FOUR_CONCEALED_TRIPLETS: {
    displayName: "Four Concealed Triplets",
    description: `
      The hand contains four closed triplets or quads, and the winning tile is
      not part of the pair.
    `,
  },
  FOUR_CONCEALED_TRIPLETS_1_SIDED_WAIT: {
    displayName: "Four Concealed Triplets 1-sided Wait",
    description: `
      The hand contains four closed triplets or quads, and the winning tile is
      part of the pair.
    `,
  },
  THREE_QUADS: {
    displayName: "Three Quads",
    description: "The hand contains three quads.",
  },
  FOUR_QUADS: {
    displayName: "Four Quads",
    description: "The hand contains four quads.",
  },

  SEVEN_PAIRS: {
    displayName: "Seven Pairs",
    description: `
      The hand consists of seven different pairs. This is a special hand
      structure.
    `,
  },
  EYES: { displayName: "Eyes", description: "The hand's pair is a 2, 5 or 8." },

  HALF_FLUSH: {
    displayName: "Half Flush",
    description: "The hand contains honour tiles and tiles from only one suit.",
  },
  FULL_FLUSH: {
    displayName: "Full Flush",
    description: `
      The hand contains tiles from only one suit, with no honour tiles.
    `,
  },
  NINE_GATES: {
    displayName: "Nine Gates",
    description: `
      The hand contains 1112345678999 in the same suit, plus one extra tile
      of that suit, and the winning tile is not the extra tile.
    `,
  },
  TRUE_NINE_GATES: {
    displayName: "True Nine Gates",
    description: `
      The hand contains 1112345678999 in the same suit, plus one extra tile
      of that suit, and the winning tile is the extra tile.
    `,
  },
  ALL_GREENS: {
    displayName: "All Greens",
    description: `
      The only tiles in the hand are 2, 3, 4, 6, 8 sticks, or the Green Dragon.
    `,
  },

  ALL_SIMPLES: {
    displayName: "All Simples",
    description: "The hand does not use any terminal or honour tiles.",
  },
  HALF_OUTSIDE_HAND: {
    displayName: "Half Outside Hand",
    description: `
      Every meld or pair in the hand uses a terminal or honour tile, and both
      terminals and honours are used.
    `,
  },
  FULLY_OUTSIDE_HAND: {
    displayName: "Fully Outside Hand",
    description: `
      Every meld or pair in the hand uses a terminal tile.
    `,
  },
  ALL_TERMINALS_AND_HONOURS: {
    displayName: "All Terminals and Honours",
    description: `
      Every tile in the hand is a terminal or honour tile, and both terminals
      and honours are used.
    `,
  },
  ALL_TERMINALS: {
    displayName: "All Terminals",
    description: `
      Every tile in the hand is a terminal tile.
    `,
  },
  THIRTEEN_ORPHANS: {
    displayName: "Thirteen Orphans",
    description: `
      The hand consists of every terminal and honour tile, plus one extra
      terminal or honour tile, and the winning tile is not the extra tile
      (this is a special hand structure).
    `,
  },
  THIRTEEN_ORPHANS_13_SIDED_WAIT: {
    displayName: "Thirteen Orphans 13-sided Wait",
    description: `
      The hand consists of every terminal and honour tile, plus one extra
      terminal or honour tile, and the winning tile is the extra tile
      (this is a special hand structure).
    `,
  },

  LITTLE_THREE_DRAGONS: {
    displayName: "Little Three Dragons",
    description: `
      The hand contains two triplets or quads of dragons,
      and a pair of the third dragon.
    `,
  },
  BIG_THREE_DRAGONS: {
    displayName: "Big Three Dragons",
    description: `
      The hand contains three triplets or quads of dragons.
    `,
  },
  FOUR_LITTLE_WINDS: {
    displayName: "Four Little Winds",
    description: `
      The hand contains three triplets or quads of winds,
      and a pair of the fourth wind.
    `,
  },
  FOUR_BIG_WINDS: {
    displayName: "Four Big Winds",
    description: `
      The hand contains four triplets or quads of winds.
    `,
  },
  ALL_HONOURS: {
    displayName: "All Honours",
    description: `
      Every tile in the hand is an honour tile.
    `,
  },

  SEAT_WIND: {
    displayName: "Seat Wind",
    description: `
      The hand contains a triplet or quad of the player seat's wind.
    `,
  },
  PREVALENT_WIND: {
    displayName: "Prevalent Wind",
    description: `
      The hand contains a triplet or quad of the wind round's wind.
    `,
  },
  NORTH_WIND: {
    displayName: "North Wind",
    description: `
      (Only applies in 3-player mahjong) The hand contains a triplet or quad of
      the North wind.
    `,
  },
  WHITE_DRAGON: {
    displayName: "White Dragon",
    description: `
      The hand contains a triplet or quad of the White Dragon.
    `,
  },
  GREEN_DRAGON: {
    displayName: "Green Dragon",
    description: `
      The hand contains a triplet or quad of the Green Dragon.
    `,
  },
  RED_DRAGON: {
    displayName: "Red Dragon",
    description: `
      The hand contains a triplet or quad of the Red Dragon.
    `,
  },
  YAKUHAI_PAIR: {
    displayName: "Yakuhai Pair",
    description: `
      The hand's pair is the player seat's wind, wind round's wind,
      or a dragon (or the North wind if playing 3-player mahjong).
    `,
  },

  SIMPLE_OPEN_TRIPLET: {
    displayName: "Simple Open Triplet",
    description: `
      This counts the number of simple open triplet melds in the hand.
    `,
  },
  ORPHAN_OPEN_TRIPLET: {
    displayName: "Orphan Open Triplet",
    description: `
      This counts the number of orphan open triplet melds in the hand.
    `,
  },
  SIMPLE_CLOSED_TRIPLET: {
    displayName: "Simple Closed Triplet",
    description: `
      This counts the number of simple closed triplet melds in the hand.
    `,
  },
  ORPHAN_CLOSED_TRIPLET: {
    displayName: "Orphan Closed Triplet",
    description: `
      This counts the number of orphan closed triplet melds in the hand.
    `,
  },
  SIMPLE_OPEN_QUAD: {
    displayName: "Simple Open Quad",
    description: `
      This counts the number of simple open quad melds in the hand.
    `,
  },
  ORPHAN_OPEN_QUAD: {
    displayName: "Orphan Open Quad",
    description: `
      This counts the number of orphan open quad melds in the hand.
    `,
  },
  SIMPLE_CLOSED_QUAD: {
    displayName: "Simple Closed Quad",
    description: `
      This counts the number of simple closed quad melds in the hand.
    `,
  },
  ORPHAN_CLOSED_QUAD: {
    displayName: "Orphan Closed Quad",
    description: `
      This counts the number of orphan closed quad melds in the hand.
    `,
  },

  NO_CALLS: {
    displayName: "No Calls",
    description: `
      The hand is closed. In other words, the only calls are closed kans or
      flowers.
    `,
  },
  NO_CALLS_TSUMO: {
    displayName: "No Calls Tsumo",
    description: `
      The hand is closed and the player drew the winning tile.
    `,
  },
  NO_CALLS_RON: {
    displayName: "No Calls Ron",
    description: `
      The hand is closed and the winning tile was discarded by another player.
    `,
  },

  NO_FLOWERS: {
    displayName: "No Flowers",
    description: `
      The hand contains no flowers.
    `,
  },
  SEAT_FLOWER: {
    displayName: "Seat Flower",
    description: `
      This counts the number of flowers that match the player's seat.
    `,
  },
  SET_OF_FLOWERS: {
    displayName: "Set of Flowers",
    description: `
      The hand contains one complete set of flowers.
    `,
  },
  FIVE_FLOWERS: {
    displayName: "Five Flowers",
    description: `
      (Only applies in 3-player mahjong) The hand contains five flowers.
    `,
  },
  SEVEN_FLOWERS: {
    displayName: "Seven Flowers",
    description: `
      The hand contains seven flowers.
    `,
  },
  TWO_SETS_OF_FLOWERS: {
    displayName: "Two Sets of Flowers",
    description: `
      The hand contains both complete sets of flowers..
    `,
  },

  OPEN_WAIT: {
    displayName: "Open Wait",
    description: `
      The winning tile is on one end of a sequence, and the other end of the
      sequence is not a terminal.
    `,
  },
  CLOSED_WAIT: {
    displayName: "Closed Wait",
    description: `
      The winning tile is in the middle of a sequence.
    `,
  },
  EDGE_WAIT: {
    displayName: "Edge Wait",
    description: `
      The winning tile is on one end of a sequence, and the other end of the
      sequence is a terminal.
    `,
  },
  DUAL_PON_WAIT: {
    displayName: "Dual Pon Wait",
    description: `
      The winning tile is part of a triplet.
    `,
  },
  PAIR_WAIT: {
    displayName: "Pair Wait",
    description: `
      The winning tile is part of a pair.
    `,
  },
} as const;

export type Pattern = (typeof patterns)[number];

export type PatternDataDict = {
  [pattern in Pattern]: PatternData;
};
