import { useId } from "preact/hooks";
import type { NumberInputProps, CheckboxInputProps } from "../input_props";

export function GameOptionsNumberInput({
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
export function GameOptionsCheckboxInput({
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
