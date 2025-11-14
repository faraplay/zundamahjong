import { useContext, useId } from "preact/hooks";

import { type GameOptions } from "../../../types/game_options";

import { Emitter } from "../../emitter/emitter";
import {
  inputPropsList,
  type CheckboxInputProps,
  type GameOptionsInputProps,
  type NumberInputProps,
} from "../input_props";
import { GameOptionsInputList } from "../game_options_input/game_options_input";
import { getPatternDataDict, PatternForm } from "../pattern_form/pattern_form";

import "./game_options_form.css";
import {
  default_3player_preset,
  default_4player_preset,
  riichi_3player_preset,
  riichi_4player_preset,
} from "../../../types/game_options_presets";
import {
  getScoreLimits,
  ScoreLimitForm,
} from "../score_limit_form/score_limit_form";

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

function getGameOptions(
  formId: string,
  patternFormId: string,
  scoreLimitFormId: string,
) {
  const formData = new FormData(
    document.getElementById(formId) as HTMLFormElement,
  );
  const formObject = {} as GameOptions;
  for (const inputProps of flattenInputPropsList(inputPropsList)) {
    if (inputProps.type == "number") {
      formObject[inputProps.name] = Number(formData.get(inputProps.name));
    } else {
      formObject[inputProps.name] = formData.has(inputProps.name);
    }
  }
  formObject.pattern_data = getPatternDataDict(patternFormId);
  formObject.base_score_limits = getScoreLimits(scoreLimitFormId);
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
  const scoreLimitFormId = useId();

  const sendGameOptions = () => {
    emit(
      "game_options",
      getGameOptions(formId, patternFormId, scoreLimitFormId),
    );
  };
  const addNewScoreLimit = () => {
    const gameOptions = getGameOptions(formId, patternFormId, scoreLimitFormId);
    gameOptions.base_score_limits.push({ han: 0, score: 0 });
    emit("game_options", gameOptions);
  };
  const removeScoreLimit = (index: number) => {
    const gameOptions = getGameOptions(formId, patternFormId, scoreLimitFormId);
    gameOptions.base_score_limits.splice(index, 1);
    emit("game_options", gameOptions);
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

  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    emit("start_game");
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
        <details
          class={`score_limit_options ${isEditable ? "can_edit" : "cannot_edit"}`}
        >
          <summary>Score limits</summary>
          <ScoreLimitForm
            scoreLimits={gameOptions.base_score_limits}
            scoreLimitFormId={scoreLimitFormId}
            isEditable={isEditable}
            addNewScoreLimit={addNewScoreLimit}
            removeScoreLimit={removeScoreLimit}
            sendGameOptions={sendGameOptions}
            onSubmit={onSubmit}
          />
        </details>
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
