import { useContext, useId } from "preact/hooks";

import { Emitter } from "../emitter/emitter";

import "./game_options_form.css";
import {
  yakuDisplayNames,
  yakus,
  type GameOptions,
  type YakuValues,
} from "../../types/game_options";
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
  const yakuFormId = useId();

  const sendGameOptions = () => {
    const formData = new FormData(
      document.getElementById(formId) as HTMLFormElement,
    );
    const yakuFormData = new FormData(
      document.getElementById(yakuFormId) as HTMLFormElement,
    );
    for (const prop of inputProps) {
      if (prop.type == "checkbox") {
        formData.set(
          prop.fieldName,
          formData.has(prop.fieldName) ? "True" : "False",
        );
      }
    }
    const formObject = Object.fromEntries(formData) as {
      [key in keyof GameOptions]: unknown;
    };
    formObject.yaku_values = Object.fromEntries(
      yakuFormData,
    ) as unknown as YakuValues;
    emit("game_options", formObject);
  };
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    emit("start_game");
  };

  const yakuInputs = yakus.map((yaku) => (
    <GameOptionsNumberInput
      key={yaku}
      isEditable={isEditable}
      props={{
        fieldName: yaku,
        labelText: yakuDisplayNames[yaku],
        type: "number",
      }}
      value={gameOptions.yaku_values[yaku]}
      formId={yakuFormId}
      sendGameOptions={sendGameOptions}
    />
  ));
  return (
    <>
      <form id={formId} onSubmit={onSubmit} />
      <form id={yakuFormId} onSubmit={onSubmit} />
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
        {yakuInputs}
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
