import { useId } from "preact/hooks";
import type { NumberInputProps } from "../input_props";

export function GameOptionsNumberInput({
  isEditable,
  inputProps,
  value,
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  inputProps: NumberInputProps;
  value: number;
  formId: string;
  sendGameOptions: () => void;
}) {
  const inputId = useId();
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const editableProps = isEditable ? { onChange } : { readonly: true };
  return (
    <>
      <label for={inputId}>{inputProps.labelText}</label>
      <input
        form={formId}
        id={inputId}
        value={value}
        {...inputProps}
        {...editableProps}
      />
    </>
  );
}
