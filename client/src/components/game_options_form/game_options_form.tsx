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
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  props: NumberInputProps;
  value: number;
  formId: string;
  sendGameOptions: () => void;
}) {
  const inputId = useId();
  const label = <label for={inputId}>{props.labelText}</label>;
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const input = isEditable ? (
    <input
      form={formId}
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
      form={formId}
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
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  props: CheckboxInputProps;
  checked: boolean;
  formId: string;
  sendGameOptions: () => void;
}) {
  const inputId = useId();
  const label = <label for={inputId}>{props.labelText}</label>;
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const input = isEditable ? (
    <input
      form={formId}
      id={inputId}
      name={props.fieldName}
      type="checkbox"
      defaultChecked={checked}
      disabled={props.readonly}
      onChange={onChange}
    />
  ) : (
    <input
      form={formId}
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
  const formId = useId();

  const sendGameOptions = () => {
    const formData = new FormData(
      document.getElementById(formId) as HTMLFormElement,
    );
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
    <>
      <form id={formId} onSubmit={onSubmit} />
      <div class="game_options">
        {inputProps.map((props) =>
          props.type == "number" ? (
            <GameOptionsNumberInput
              key={props.fieldName}
              isEditable={isEditable}
              props={props}
              value={gameOptions[props.fieldName]}
              formId={formId}
              sendGameOptions={sendGameOptions}
            />
          ) : (
            <GameOptionsCheckboxInput
              key={props.fieldName}
              isEditable={isEditable}
              props={props}
              checked={gameOptions[props.fieldName]}
              formId={formId}
              sendGameOptions={sendGameOptions}
            />
          ),
        )}
        <button
          type="submit"
          class="start_game"
          form={formId}
          disabled={!can_start}
        >
          Start game
        </button>
      </div>
    </>
  );
}
