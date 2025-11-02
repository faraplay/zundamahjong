import { useContext, useId } from "preact/hooks";

import {
  patternDisplayNames,
  patterns,
  type GameOptions,
  type PatternDataDict,
} from "../../../types/game_options";

import { Emitter } from "../../emitter/emitter";
import {
  inputPropsList,
  type CheckboxInputProps,
  type GameOptionsInputProps,
  type NumberInputProps,
} from "../input_props";
import { GameOptionsInputList } from "../game_options_input/game_options_input";
import { PatternForm } from "../pattern_form/pattern_form";

import "./game_options_form.css";
import {
  default_3player_preset,
  default_4player_preset,
  riichi_3player_preset,
  riichi_4player_preset,
} from "../../../types/game_options_presets";

function flattenInputPropsList(propsList: GameOptionsInputProps[]) {
  const newPropsList: (NumberInputProps | CheckboxInputProps)[] = [];
  for (const props of propsList) {
    if (props.type == "collection") {
      newPropsList.push(...flattenInputPropsList(props.children));
    } else {
      newPropsList.push(props);
    }
  }
  return newPropsList;
}

function getGameOptions(formId: string, patternFormId: string) {
  const formData = new FormData(
    document.getElementById(formId) as HTMLFormElement,
  );
  const patternFormData = new FormData(
    document.getElementById(patternFormId) as HTMLFormElement,
  );
  const formObject = {} as GameOptions;
  for (const inputProps of flattenInputPropsList(inputPropsList)) {
    if (inputProps.type == "number") {
      formObject[inputProps.name] = Number(formData.get(inputProps.name));
    } else {
      formObject[inputProps.name] = formData.has(inputProps.name);
    }
  }
  formObject.pattern_data = Object.fromEntries(
    patterns.map((pattern) => [
      pattern,
      {
        display_name: patternDisplayNames[pattern],
        han: Number(patternFormData.get(`${pattern}___han`)),
        fu: Number(patternFormData.get(`${pattern}___fu`)),
      },
    ]),
  ) as PatternDataDict;
  return formObject;
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
  const patternFormId = useId();

  const sendGameOptions = () => {
    emit("game_options", getGameOptions(formId, patternFormId));
  };
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    emit("start_game");
  };
  const sendDefaultPresetGameOptions = (e: Event) => {
    e.preventDefault();
    if (gameOptions.player_count == 4) {
      emit("game_options", default_4player_preset);
    } else {
      emit("game_options", default_3player_preset);
    }
  };
  const sendRiichiPresetGameOptions = (e: Event) => {
    e.preventDefault();
    if (gameOptions.player_count == 4) {
      emit("game_options", riichi_4player_preset);
    } else {
      emit("game_options", riichi_3player_preset);
    }
  };

  return (
    <div class="game_controls">
      {isEditable ? (
        <div class="presets">
          <button type="button" onClick={sendDefaultPresetGameOptions}>
            Use default preset
          </button>
          <button type="button" onClick={sendRiichiPresetGameOptions}>
            Use riichi preset
          </button>
        </div>
      ) : (
        <></>
      )}
      <form id={formId} onSubmit={onSubmit} hidden />
      <form id={patternFormId} onSubmit={onSubmit} hidden />
      <div class="game_options">
        <GameOptionsInputList
          inputPropsList={inputPropsList}
          gameOptions={gameOptions}
          isEditable={isEditable}
          formId={formId}
          sendGameOptions={sendGameOptions}
        />
        <details class="pattern_options">
          <summary>Patterns</summary>
          <div class="table_header">
            <div>Pattern</div>
            <div>Han</div>
            <div>Fu</div>
          </div>
          <PatternForm
            patternValues={gameOptions.pattern_data}
            patternFormId={patternFormId}
            isEditable={isEditable}
            sendGameOptions={sendGameOptions}
          />
        </details>
      </div>
      <button
        type="submit"
        class="start_game"
        form={formId}
        disabled={!(isEditable && can_start)}
      >
        Start game
      </button>
    </div>
  );
}
