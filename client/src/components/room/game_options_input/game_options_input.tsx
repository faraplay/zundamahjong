import type { GameOptionsInputProps, InputExpanderProps } from "../input_props";
import type { GameOptions } from "../../../types/game_options";
import { GameOptionsNumberInput } from "./number_input";
import { GameOptionsCheckboxInput } from "./checkbox_input";

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
    <details class="game_options_expander">
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
