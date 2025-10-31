import { useId } from "preact/hooks";
import type {
  NumberInputProps,
  CheckboxInputProps,
  GameOptionsInputProps,
  InputExpanderProps,
} from "../input_props";
import type {
  GameOptions,
  Pattern,
  PatternData,
} from "../../../types/game_options";

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

function getEditableProps<T>(
  value: T,
  isEditable: boolean,
  onChange: (e: Event) => void,
) {
  return isEditable
    ? {
        defaultValue: value,
        onChange,
      }
    : {
        value,
        readonly: true,
      };
}

export function GameOptionsPatternInput({
  isEditable,
  name,
  data,
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  name: Pattern;
  data: PatternData;
  formId: string;
  sendGameOptions: () => void;
}) {
  console.log(data);
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const hanEditableProps = getEditableProps(data.han, isEditable, onChange);
  const fuEditableProps = getEditableProps(data.fu, isEditable, onChange);
  return (
    <>
      <label>{data.display_name}</label>
      <input
        form={formId}
        name={`${name}___han`}
        type="number"
        {...hanEditableProps}
      />
      <input
        form={formId}
        name={`${name}___fu`}
        type="number"
        {...fuEditableProps}
      />
    </>
  );
}

export function GameOptionsInputExpander({
  isEditable,
  inputProps,
  gameOptions,
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  inputProps: InputExpanderProps;
  gameOptions: GameOptions;
  formId: string;
  sendGameOptions: () => void;
}) {
  return (
    <details>
      <summary>{inputProps.name}</summary>
      <GameOptionsInputList
        isEditable={isEditable}
        formId={formId}
        sendGameOptions={sendGameOptions}
        inputPropsList={inputProps.children}
        gameOptions={gameOptions}
      />
    </details>
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
  inputPropsList: GameOptionsInputProps[];
  gameOptions: GameOptions;
  formId: string;
  sendGameOptions: () => void;
}) {
  return inputPropsList.map((inputProps) =>
    inputProps.type == "number" ? (
      <GameOptionsNumberInput
        key={inputProps.name}
        isEditable={isEditable}
        formId={formId}
        sendGameOptions={sendGameOptions}
        inputProps={inputProps}
        value={gameOptions[inputProps.name]}
      />
    ) : inputProps.type == "checkbox" ? (
      <GameOptionsCheckboxInput
        key={inputProps.name}
        isEditable={isEditable}
        formId={formId}
        sendGameOptions={sendGameOptions}
        inputProps={inputProps}
        value={gameOptions[inputProps.name]}
      />
    ) : (
      <GameOptionsInputExpander
        key={inputProps.name}
        isEditable={isEditable}
        formId={formId}
        sendGameOptions={sendGameOptions}
        inputProps={inputProps}
        gameOptions={gameOptions}
      />
    ),
  );
}
