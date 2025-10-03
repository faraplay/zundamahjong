import { useContext, useId } from "preact/hooks";

import { Emitter } from "../emitter/emitter";

import "./game_options_form.css";

type NumberInputProps = {
  fieldName: string;
  labelText: string;
  type: "number";
  min?: number;
  max?: number;
  step?: number;
  readonly?: boolean;
};

type CheckboxInputProps = {
  fieldName: string;
  labelText: string;
  type: "checkbox";
  value?: "True";
  readonly?: boolean;
};

function GameOptionsNumberInput({
  props,
  value,
}: {
  props: NumberInputProps;
  value: number;
}) {
  const inputId = useId();
  const label = <label for={inputId}>{props.labelText}</label>;
  const input = (
    <input
      id={inputId}
      name={props.fieldName}
      type={props.type}
      defaultValue={value}
      min={props.min}
      max={props.max}
      step={props.step}
      readonly={props.readonly}
    />
  );
  return (
    <>
      {label}
      {input}
    </>
  );
}

function GameOptionsCheckboxInput({
  props,
  checked,
}: {
  props: CheckboxInputProps;
  checked: boolean;
}) {
  const inputId = useId();
  const label = <label for={inputId}>{props.labelText}</label>;
  const input = (
    <input
      id={inputId}
      name={props.fieldName}
      type={props.type}
      value={props.value}
      checked={checked}
      readonly={props.readonly}
    />
  );
  return (
    <>
      {label}
      {input}
    </>
  );
}

const inputProps = [
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
    value: "True",
  },
] as const;

export function GameOptionsForm({
  player_count,
  can_start,
}: {
  player_count: number;
  can_start: boolean;
}) {
  const emit = useContext(Emitter);
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    emit("start_game", Object.fromEntries(formData));
  };
  const inputValues = {
    player_count,
    game_length_wind_rounds: 1,
    game_length_sub_rounds: 0,
    score_dealer_ron_base_value: 1.5,
    score_dealer_tsumo_base_value: 1.0,
    score_nondealer_ron_base_value: 1.0,
    score_nondealer_tsumo_nondealer_base_value: 0.5,
    score_nondealer_tsumo_dealer_base_value: 1.0,
    auto_replace_flowers: "True",
  } as const;
  return (
    <form id="game_options_form" onSubmit={onSubmit}>
      {inputProps.map((props) =>
        props.type == "number" ? (
          <GameOptionsNumberInput
            key={props.fieldName}
            props={props}
            value={inputValues[props.fieldName]}
          />
        ) : (
          <GameOptionsCheckboxInput
            key={props.fieldName}
            props={props}
            checked={inputValues[props.fieldName] == "True"}
          />
        ),
      )}
      <button type="submit" id="start_game" disabled={!can_start}>
        Start game
      </button>
    </form>
  );
}
