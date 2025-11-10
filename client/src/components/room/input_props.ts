import type { GameOptions } from "../../types/game_options";

type GameOptionsOfValueType<T> = {
  [key in keyof GameOptions as GameOptions[key] extends T ? key : never]: T;
};

export type NumberInputProps = {
  name: keyof GameOptionsOfValueType<number>;
  labelText: string;
  type: "number";
  min?: number;
  max?: number;
  step?: number;
  readonly?: boolean;
};

export type CheckboxInputProps = {
  name: keyof GameOptionsOfValueType<boolean>;
  labelText: string;
  type: "checkbox";
  disabled?: boolean;
};

export type InputExpanderProps = {
  type: "collection";
  name: string;
  children: GameOptionsInputProps[];
};

export type GameOptionsInputProps =
  | NumberInputProps
  | CheckboxInputProps
  | InputExpanderProps;

export const inputPropsList: GameOptionsInputProps[] = [
  {
    name: "player_count",
    labelText: "Number of players",
    type: "number",
    readonly: true,
  },
  {
    name: "game_length_wind_rounds",
    labelText: "Number of wind rounds",
    type: "number",
    min: 0,
    max: 4,
  },
  {
    name: "game_length_sub_rounds",
    labelText: "Number of sub rounds",
    type: "number",
    min: 0,
    max: 3,
  },
  {
    name: "use_flowers",
    labelText: "Use flowers",
    type: "checkbox",
  },
  {
    name: "auto_replace_flowers",
    labelText: "Auto flowers",
    type: "checkbox",
  },
  {
    name: "end_wall_count",
    labelText: "Number of tiles in dead wall",
    type: "number",
    min: 0,
  },
  {
    name: "min_han",
    labelText: "Minimum han to win",
    type: "number",
    min: 0,
  },
  {
    name: "allow_riichi",
    labelText: "Allow riichi",
    type: "checkbox",
  },
  {
    name: "show_waits",
    labelText: "Show waits",
    type: "checkbox",
  },
  {
    name: "show_shanten_info",
    labelText: "Show shanten info",
    type: "checkbox",
  },
  {
    type: "collection",
    name: "Base Scores",
    children: [
      {
        name: "start_score",
        labelText: "Starting score",
        type: "number",
      },
      {
        name: "score_dealer_ron_multiplier",
        labelText: "Dealer ron base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_dealer_tsumo_multiplier",
        labelText: "Dealer tsumo base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_ron_multiplier",
        labelText: "Nondealer ron base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_tsumo_nondealer_multiplier",
        labelText: "Nondealer-nondealer tsumo base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_tsumo_dealer_multiplier",
        labelText: "Nondealer-dealer tsumo base score",
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
        type: "checkbox",
      },
      {
        name: "base_fu",
        labelText: "Base fu",
        type: "number",
        step: 1,
      },
      {
        name: "round_up_fu",
        labelText: "Round up fu",
        type: "checkbox",
      },
      {
        name: "round_up_points",
        labelText: "Round up points",
        type: "checkbox",
      },
    ],
  },
] as const;
