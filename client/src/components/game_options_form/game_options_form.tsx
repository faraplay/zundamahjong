import { useContext, useId } from "preact/hooks";

import { Emitter } from "../emitter/emitter";

import "./game_options_form.css";
import type { GameOptions } from "../../types/game_options";
import {
  inputProps,
  type CheckboxInputProps,
  type NumberInputProps,
} from "./input_props";

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
