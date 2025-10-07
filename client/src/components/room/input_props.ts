import type { GameOptions, Yaku } from "../../types/game_options";

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

export type YakuInputProps = {
  name: Yaku;
  labelText: string;
  type: "number";
  min?: number;
  max?: number;
  step?: number;
  readonly?: boolean;
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
    name: "auto_replace_flowers",
    labelText: "Auto flowers",
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
        name: "score_dealer_ron_base_value",
        labelText: "Dealer ron base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_dealer_tsumo_base_value",
        labelText: "Dealer tsumo base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_ron_base_value",
        labelText: "Nondealer ron base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_tsumo_nondealer_base_value",
        labelText: "Nondealer-nondealer tsumo base score",
        type: "number",
        step: 0.5,
      },
      {
        name: "score_nondealer_tsumo_dealer_base_value",
        labelText: "Nondealer-dealer tsumo base score",
        type: "number",
        step: 0.5,
      },
    ],
  },
] as const;
