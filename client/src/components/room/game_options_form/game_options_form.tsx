import { useContext, useId } from "preact/hooks";

import {
  patternDisplayNames,
  patterns,
  type GameOptions,
} from "../../../types/game_options";

import { Emitter } from "../../emitter/emitter";
import { inputPropsList } from "../input_props";
import { GameOptionsInputList } from "../game_options_input/game_options_input";
import { PatternForm } from "../pattern_form/pattern_form";

import "./game_options_form.css";

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
    const formData = new FormData(
      document.getElementById(formId) as HTMLFormElement,
    );
    const patternFormData = new FormData(
      document.getElementById(patternFormId) as HTMLFormElement,
    );
    for (const inputProps of inputPropsList) {
      if (inputProps.type == "checkbox") {
        formData.set(
          inputProps.name,
          formData.has(inputProps.name) ? "True" : "False",
        );
      }
    }
    const formObject = Object.fromEntries(formData) as {
      [key in keyof GameOptions]: unknown;
    };
    formObject.pattern_data = Object.fromEntries(
      patterns.map((pattern) => [
        pattern,
        {
          display_name: patternDisplayNames[pattern],
          han: Number(patternFormData.get(`${pattern}___han`)),
          fu: Number(patternFormData.get(`${pattern}___fu`)),
        },
      ]),
    );

    emit("game_options", formObject);
  };
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    emit("start_game");
  };

  return (
    <div class="game_controls">
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
