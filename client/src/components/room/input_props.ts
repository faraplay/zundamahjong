import type { GameOptions, Yaku } from "../../types/game_options";

type GameOptionsOfValueType<T> = {
  [key in keyof GameOptions as GameOptions[key] extends T ? key : never]: T;
};

export type NumberInputProps = {
  fieldName: keyof GameOptionsOfValueType<number>;
  labelText: string;
  type: "number";
  min?: number;
  max?: number;
  step?: number;
  readonly?: boolean;
};

export type CheckboxInputProps = {
  fieldName: keyof GameOptionsOfValueType<boolean>;
  labelText: string;
  type: "checkbox";
  readonly?: boolean;
};

export type YakuInputProps = {
  fieldName: Yaku;
  labelText: string;
  type: "number";
  min?: number;
  max?: number;
  step?: number;
  readonly?: boolean;
};

export const inputProps: (NumberInputProps | CheckboxInputProps)[] = [
  {
    fieldName: "player_count",
    labelText: "Number of players",
    type: "number",
    readonly: true,
  },
  {
    fieldName: "game_length_wind_rounds",
    labelText: "Number of wind rounds",
    type: "number",
    min: 0,
    max: 4,
  },
  {
    fieldName: "game_length_sub_rounds",
    labelText: "Number of sub rounds",
    type: "number",
    min: 0,
    max: 3,
  },
  {
    fieldName: "score_dealer_ron_base_value",
    labelText: "Dealer ron base score",
    type: "number",
    step: 0.5,
  },
  {
    fieldName: "score_dealer_tsumo_base_value",
    labelText: "Dealer tsumo base score",
    type: "number",
    step: 0.5,
  },
  {
    fieldName: "score_nondealer_ron_base_value",
    labelText: "Nondealer ron base score",
    type: "number",
    step: 0.5,
  },
  {
    fieldName: "score_nondealer_tsumo_nondealer_base_value",
    labelText: "Nondealer-nondealer tsumo base score",
    type: "number",
    step: 0.5,
  },
  {
    fieldName: "score_nondealer_tsumo_dealer_base_value",
    labelText: "Nondealer-dealer tsumo base score",
    type: "number",
    step: 0.5,
  },
  {
    fieldName: "auto_replace_flowers",
    labelText: "Auto flowers",
    type: "checkbox",
  },
] as const;
