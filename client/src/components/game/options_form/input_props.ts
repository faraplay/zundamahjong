import type { ClientOptions } from "../../../types/client_options";
import type { GameOptions } from "../../../types/game_options";

type OptionsOfValueType<Options, Value> = {
  [key in keyof Options as Options[key] extends Value ? key : never]: Value;
};

export type InputLabelProps = {
  labelText: string;
  description: string;
  subDescription?: string;
};

export type NumberInputProps<Options> = InputLabelProps & {
  name: keyof OptionsOfValueType<Options, number>;
  type: "number";
  min?: number;
  max?: number;
  step?: number;
  readonly?: boolean;
};

export type CheckboxInputProps<Options> = InputLabelProps & {
  name: keyof OptionsOfValueType<Options, boolean>;
  type: "checkbox";
  disabled?: boolean;
};

export type InputExpanderProps<Options> = {
  type: "collection";
  name: string;
  children: OptionsInputProps<Options>[];
};

export type OptionsInputProps<Options> =
  | NumberInputProps<Options>
  | CheckboxInputProps<Options>
  | InputExpanderProps<Options>;

export const clientInputPropsList: OptionsInputProps<ClientOptions>[] = [
  {
    name: "show_tile_numbers",
    labelText: "Show tile numbers",
    description: "Show tile numbers in the corners of tiles",
    type: "checkbox",
  },
];

export const inputPropsList: OptionsInputProps<GameOptions>[] = [
  {
    name: "player_count",
    labelText: "Number of players",
    description: "The number of players in the game of mahjong.",
    type: "number",
    readonly: true,
  },
  {
    name: "game_length_wind_rounds",
    labelText: "Number of wind rounds",
    description: "The number of wind rounds to play in the game of mahjong.",
    subDescription: `One wind round of mahjong is the series of rounds it takes
      for each player to play as dealer. The number of rounds in one wind round
      is at minimum the number of players, but can be more if there are dealer
      repeats.`,
    type: "number",
    min: 0,
    max: 4,
  },
  {
    name: "game_length_sub_rounds",
    labelText: "Number of sub rounds",
    description: `The number of sub rounds to play in the game of mahjong,
      in addition to the wind rounds.`,
    subDescription: `One sub round of mahjong is a series of rounds under the
      same dealer player.`,
    type: "number",
    min: 0,
    max: 3,
  },
  {
    type: "collection",
    name: "Rules options",
    children: [
      {
        name: "use_flowers",
        labelText: "Use flowers",
        description: "Include flower tiles in the mahjong deck.",
        type: "checkbox",
      },
      {
        name: "end_wall_count",
        labelText: "Number of tiles in dead wall",
        description: `The number of tiles to leave in the dead wall.`,
        subDescription: `The round of mahjong ends in a draw if there are no
          tiles left to draw except for those in the dead wall.`,
        type: "number",
        min: 0,
      },
      {
        name: "min_han",
        labelText: "Minimum han to win",
        description: `The minimum number of han in a winning hand for a player
          to be able to win.`,
        type: "number",
        min: 0,
      },
      {
        name: "allow_riichi",
        labelText: "Allow riichi",
        description: `Allow players to call riichi if they are one tile away
          from a winning hand.`,
        subDescription:
          "A player in riichi cannot change their hand, but wins more points.",
        type: "checkbox",
      },
      {
        name: "allow_rob_added_kan",
        labelText: "Allow robbing an added kan",
        description: "Allow players to rob an added kan.",
        subDescription: `If a player calls an added kan and the tile they are
          adding is another player's winning tile, then that player can rob the
          kan and win off of that tile as if it was a discard.`,
        type: "checkbox",
      },
      {
        name: "allow_thirteen_orphans_rob_closed_kan",
        labelText: "Allow robbing a closed kan to form thirteen orphans",
        description: "Allow players to rob a closed kan for thirteen orphans.",
        subDescription: `If a player calls a closed kan and the tile in the kan
          is the winning tile another player needs to form a thirteen orphans
          hand, then that player can rob the kan and win off of that tile as if
          it was a discard.`,
        type: "checkbox",
      },
      {
        name: "allow_rob_closed_kan",
        labelText: "Allow robbing a closed kan",
        description: "Allow players to rob a closed kan.",
        subDescription: `If a player calls a closed kan and the tile in the kan
          is another player's winning tile, then that player can rob the kan and
          win off of that tile as if it was a discard.`,
        type: "checkbox",
      },
      {
        name: "use_temporary_furiten",
        labelText: "Use temporary furiten",
        description: `Prevents a player's ron (winning off another player's
          discard) if they are in temporary furiten.`,
        subDescription: `A player is in temporary furiten if they can form a
          winning hand from any tile previously discarded since their last
          discard.`,
        type: "checkbox",
      },
      {
        name: "use_riichi_furiten",
        labelText: "Use riichi furiten",
        description: `Prevents a player's ron (winning off another player's
          discard) if they are in riichi furiten.`,
        subDescription: `A player is in riichi furiten if they are in riichi
          and can form a winning hand from any tile previously discarded
          since they called riichi.`,
        type: "checkbox",
      },
      {
        name: "use_own_discard_furiten",
        labelText: "Use own-discard furiten",
        description: `Prevents a player's ron (winning off another player's
          discard) if they are in own-discard furiten.`,
        subDescription: `A player is in own-discard furiten if they can form a
          winning hand from any of their own discards.`,
        type: "checkbox",
      },
    ],
  },
  {
    type: "collection",
    name: "Quality-of-life options",
    children: [
      {
        name: "auto_replace_flowers",
        labelText: "Automatically replace flowers",
        description: "Automatically performs flower calls for all players.",
        type: "checkbox",
      },
      {
        name: "show_waits",
        labelText: "Show waits",
        description: "Show each player their own waits if they are in tenpai.",
        subDescription: `A player is in tenpai if they are one tile away from
          a winning hand. The player's waits are the tiles they can take to
          form a winning hand.`,
        type: "checkbox",
      },
      {
        name: "show_shanten_info",
        labelText: "Show shanten info",
        description: `Show each player their shanten, and which tiles decrease
          their shanten.`,
        subDescription: `A player's shanten is the minimum number of tiles they
          need to replace in their hand to reach tenpai (one tile away from
          winning).`,
        type: "checkbox",
      },
    ],
  },
  {
    type: "collection",
    name: "Base Scores",
    children: [
      {
        name: "start_score",
        labelText: "Starting score",
        description: "The score each player starts with.",
        type: "number",
      },
      {
        name: "score_dealer_ron_multiplier",
        labelText: "Dealer ron base score multiplier",
        description: `If the dealer wins off another player's discard, then
          the base score is multiplied by this number to calculate the amount
          the losing player must pay the dealer.`,
        subDescription: `The base score is calculated using the formula
          (base score) = 4 * (fu) * 2^(han)`,
        type: "number",
        step: 0.5,
      },
      {
        name: "score_dealer_tsumo_multiplier",
        labelText: "Dealer tsumo base score multiplier",
        description: `If the dealer wins from their own draw, then
          the base score is multiplied by this number to calculate the amount
          each losing player must pay the dealer.`,
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_ron_multiplier",
        labelText: "Nondealer ron base score multiplier",
        description: `If a non-dealer wins off another player's discard, then
          the base score is multiplied by this number to calculate the amount
          the losing player must pay the winning player.`,
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_tsumo_nondealer_multiplier",
        labelText: "Nondealer-nondealer tsumo base score multiplier",
        description: `If a non-dealer wins from their own draw, then
          the base score is multiplied by this number to calculate the amount
          a non-dealer losing player must pay the winning player.`,
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_tsumo_dealer_multiplier",
        labelText: "Nondealer-dealer tsumo base score multiplier",
        description: `If a non-dealer wins from their own draw, then
          the base score is multiplied by this number to calculate the amount
          the dealer must pay the winning player.`,
        type: "number",
        step: 0.5,
      },
    ],
  },
  {
    type: "collection",
    name: "Fu options",
    children: [
      {
        name: "calculate_fu",
        labelText: "Calculate fu",
        description: "Add fu to a player's scoring calculation when they win.",
        subDescription: `If unset, the fu value used in score calculation will
          always be the base fu value.`,
        type: "checkbox",
      },
      {
        name: "base_fu",
        labelText: "Base fu",
        description: "The base fu value every winning hand starts with.",
        subDescription: `Any additional fu in a winning hand is added to this
          base fu value.`,
        type: "number",
        step: 1,
      },
      {
        name: "round_up_fu",
        labelText: "Round up fu",
        description:
          "Round up a winning player's fu to the next multiple of 10.",
        type: "checkbox",
      },
      {
        name: "round_up_points",
        labelText: "Round up points",
        description: `Round up a winning player's point gain from each player to
          the next multiple of 100.`,
        type: "checkbox",
      },
    ],
  },
] as const;
