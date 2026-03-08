import { useId } from "preact/hooks";
import type { CheckboxInputProps } from "../input_props";

export function OptionsCheckboxInput<Options>({
  isEditable,
  inputProps,
  value,
  formId,
  setOptions,
}: {
  isEditable: boolean;
  inputProps: CheckboxInputProps<Options>;
  value: boolean;
  formId: string;
  setOptions: () => void;
}) {
  const inputId = useId();
  const onChange = (e: Event) => {
    e.preventDefault();
    setOptions();
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
