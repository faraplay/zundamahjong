import { useId } from "preact/hooks";
import type { CheckboxInputProps } from "../input_props";

export function GameOptionsCheckboxInput({
  isEditable,
  inputProps,
  value,
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  inputProps: CheckboxInputProps;
  value: boolean;
  formId: string;
  sendGameOptions: () => void;
}) {
  const inputId = useId();
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const editableProps = isEditable ? { onChange } : { disabled: true };
  return (
    <>
      <label for={inputId}>{inputProps.labelText}</label>
      <input
        form={formId}
        id={inputId}
        checked={value}
        {...inputProps}
        {...editableProps}
      />
    </>
  );
}
