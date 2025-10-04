import { useContext, useId } from "preact/hooks";

import { Emitter } from "../emitter/emitter";

import "./game_options_form.css";
import type { GameOptions } from "../../types/game_options";

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
  readonly?: boolean;
};

function GameOptionsNumberInput({
  isEditable,
  props,
  value,
  sendGameOptions,
}: {
  isEditable: boolean;
  props: NumberInputProps;
  value: number;
  sendGameOptions: (form: HTMLFormElement) => void;
}) {
  const inputId = useId();
  const label = <label for={inputId}>{props.labelText}</label>;
  const onChange = (e: Event) => {
    e.preventDefault();
    const form = (e.currentTarget as HTMLInputElement).form;
    if (form) {
      sendGameOptions(form);
    }
  };
  const input = isEditable ? (
    <input
      id={inputId}
      name={props.fieldName}
      type="number"
      defaultValue={value}
      min={props.min}
      max={props.max}
      step={props.step}
      readonly={props.readonly}
      onChange={onChange}
    />
  ) : (
    <input
      id={inputId}
      name={props.fieldName}
      type="number"
      value={value}
      readonly
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
  isEditable,
  props,
  checked,
  sendGameOptions,
}: {
  isEditable: boolean;
  props: CheckboxInputProps;
  checked: boolean;
  sendGameOptions: (form: HTMLFormElement) => void;
}) {
  const inputId = useId();
  const label = <label for={inputId}>{props.labelText}</label>;
  const onChange = (e: Event) => {
    e.preventDefault();
    const form = (e.currentTarget as HTMLInputElement).form;
    if (form) {
      sendGameOptions(form);
    }
  };
  const input = isEditable ? (
    <input
      id={inputId}
      name={props.fieldName}
      type="checkbox"
      defaultChecked={checked}
      disabled={props.readonly}
      onChange={onChange}
    />
  ) : (
    <input
      id={inputId}
      class={`checked_${checked}`}
      name={props.fieldName}
      type="checkbox"
      checked={checked}
      disabled
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
  },
] as const;

export function GameOptionsForm({
  gameOptions,
  isEditable,
  can_start,
}: {
  gameOptions: GameOptions;
  isEditable: boolean;
  can_start: boolean;
}) {
  const emit = useContext(Emitter);
  const sendGameOptions = (form: HTMLFormElement) => {
    const formData = new FormData(form);
    for (const prop of inputProps) {
      if (prop.type == "checkbox") {
        formData.set(
          prop.fieldName,
          formData.has(prop.fieldName) ? "True" : "False",
        );
      }
    }
    emit("game_options", Object.fromEntries(formData));
  };
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    emit("start_game");
  };
  return (
    <form id="game_options_form" onSubmit={onSubmit}>
      {inputProps.map((props) =>
        props.type == "number" ? (
          <GameOptionsNumberInput
            key={props.fieldName}
            isEditable={isEditable}
            props={props}
            value={gameOptions[props.fieldName]}
            sendGameOptions={sendGameOptions}
          />
        ) : (
          <GameOptionsCheckboxInput
            key={props.fieldName}
            isEditable={isEditable}
            props={props}
            checked={gameOptions[props.fieldName]}
            sendGameOptions={sendGameOptions}
          />
        ),
      )}
      <button type="submit" id="start_game" disabled={!can_start}>
        Start game
      </button>
    </form>
  );
}
