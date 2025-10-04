import { useId } from "preact/hooks";
import type {
  NumberInputProps,
  CheckboxInputProps,
  YakuInputProps,
} from "../input_props";
import type { GameOptions } from "../../../types/game_options";

export function GameOptionsNumberInput({
  isEditable,
  inputProps,
  value,
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  inputProps: NumberInputProps | YakuInputProps;
  value: number;
  formId: string;
  sendGameOptions: () => void;
}) {
  const inputId = useId();
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const editableProps = isEditable
    ? {
        defaultValue: value,
        onChange,
      }
    : {
        value,
        readonly: true,
      };
  return (
    <>
      <label for={inputId}>{inputProps.labelText}</label>
      <input form={formId} id={inputId} {...inputProps} {...editableProps} />
    </>
  );
}

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
  const editableProps = isEditable
    ? {
        defaultChecked: value,
        onChange,
      }
    : {
        checked: value,
        disabled: true,
      };
  return (
    <>
      <label for={inputId}>{inputProps.labelText}</label>
      <input form={formId} id={inputId} {...inputProps} {...editableProps} />
    </>
  );
}

export function GameOptionsInputList({
  isEditable,
  inputPropsList,
  gameOptions,
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  inputPropsList: (NumberInputProps | CheckboxInputProps)[];
  gameOptions: GameOptions;
  formId: string;
  sendGameOptions: () => void;
}) {
  return (
    <>
      {inputPropsList.map((inputProps) =>
        inputProps.type == "number" ? (
          <GameOptionsNumberInput
            key={inputProps.name}
            isEditable={isEditable}
            formId={formId}
            sendGameOptions={sendGameOptions}
            inputProps={inputProps}
            value={gameOptions[inputProps.name]}
          />
        ) : (
          <GameOptionsCheckboxInput
            key={inputProps.name}
            isEditable={isEditable}
            formId={formId}
            sendGameOptions={sendGameOptions}
            inputProps={inputProps}
            value={gameOptions[inputProps.name]}
          />
        ),
      )}
    </>
  );
}
