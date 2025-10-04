export const inputProps = [
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
export type NumberInputProps = {
  fieldName: string;
  labelText: string;
  type: "number";
  min?: number;
  max?: number;
  step?: number;
  readonly?: boolean;
};
export type CheckboxInputProps = {
  fieldName: string;
  labelText: string;
  type: "checkbox";
  readonly?: boolean;
};
