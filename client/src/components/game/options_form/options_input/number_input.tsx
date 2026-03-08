import { useId } from "preact/hooks";
import type { NumberInputProps } from "../input_props";

export function OptionsNumberInput<Options>({
  isEditable,
  inputProps,
  value,
  formId,
  setOptions,
}: {
  isEditable: boolean;
  inputProps: NumberInputProps<Options>;
  value: number;
  formId: string;
  setOptions: () => void;
}) {
  const inputId = useId();
  const onChange = (e: Event) => {
    e.preventDefault();
    setOptions();
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
