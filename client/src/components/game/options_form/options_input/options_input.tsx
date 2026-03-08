import type {
  OptionsInputProps,
  InputExpanderProps,
  CheckboxInputProps,
  NumberInputProps,
} from "../input_props";
import { OptionsNumberInput } from "./number_input";
import { OptionsCheckboxInput } from "./checkbox_input";

export function OptionsInputExpander<Options>({
  isEditable,
  inputProps,
  options,
  formId,
  setOptions,
}: {
  isEditable: boolean;
  inputProps: InputExpanderProps<Options>;
  options: Options;
  formId: string;
  setOptions: () => void;
}) {
  return (
    <details class="options_expander">
      <summary>{inputProps.name}</summary>
      <OptionsInputList
        isEditable={isEditable}
        formId={formId}
        setOptions={setOptions}
        inputPropsList={inputProps.children}
        options={options}
      />
    </details>
  );
}

export function OptionsInputList<Options>({
  isEditable,
  inputPropsList,
  options,
  formId,
  setOptions,
}: {
  isEditable: boolean;
  inputPropsList: OptionsInputProps<Options>[];
  options: Options;
  formId: string;
  setOptions: () => void;
}) {
  return inputPropsList.map((inputProps) =>
    inputProps.type == "number" ? (
      <OptionsNumberInput
        key={inputProps.name}
        isEditable={isEditable}
        formId={formId}
        setOptions={setOptions}
        inputProps={inputProps}
        value={options[inputProps.name] as number}
      />
    ) : inputProps.type == "checkbox" ? (
      <OptionsCheckboxInput
        key={inputProps.name}
        isEditable={isEditable}
        formId={formId}
        setOptions={setOptions}
        inputProps={inputProps}
        value={options[inputProps.name] as boolean}
      />
    ) : (
      <OptionsInputExpander
        key={inputProps.name}
        isEditable={isEditable}
        formId={formId}
        setOptions={setOptions}
        inputProps={inputProps}
        options={options}
      />
    ),
  );
}

export function flattenInputPropsList<Options>(
  propsList: OptionsInputProps<Options>[],
) {
  const newPropsList: (
    | NumberInputProps<Options>
    | CheckboxInputProps<Options>
  )[] = [];
  for (const props of propsList) {
    if (props.type == "collection") {
      newPropsList.push(...flattenInputPropsList(props.children));
    } else {
      newPropsList.push(props);
    }
  }
  return newPropsList;
}
