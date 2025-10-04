import { useContext, useId } from "preact/hooks";

import { type GameOptions, type YakuValues } from "../../../types/game_options";

import { Emitter } from "../../emitter/emitter";
import { inputPropsList } from "../input_props";
import { GameOptionsInputList } from "../game_options_input/game_options_input";
import { YakuForm } from "../yaku_form/yaku_form";

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
  const yakuFormId = useId();

  const sendGameOptions = () => {
    const formData = new FormData(
      document.getElementById(formId) as HTMLFormElement,
    );
    const yakuFormData = new FormData(
      document.getElementById(yakuFormId) as HTMLFormElement,
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
    formObject.yaku_values = Object.fromEntries(
      yakuFormData,
    ) as unknown as YakuValues;
    emit("game_options", formObject);
  };
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    emit("start_game");
  };

  return (
    <>
      <form id={formId} onSubmit={onSubmit} hidden />
      <form id={yakuFormId} onSubmit={onSubmit} hidden />
      <div class="game_options">
        <GameOptionsInputList
          inputPropsList={inputPropsList}
          gameOptions={gameOptions}
          isEditable={isEditable}
          formId={formId}
          sendGameOptions={sendGameOptions}
        />
        <details>
          <summary>Yaku</summary>
          <YakuForm
            yakuValues={gameOptions.yaku_values}
            yakuFormId={yakuFormId}
            isEditable={isEditable}
            sendGameOptions={sendGameOptions}
          />
        </details>
        <button
          type="submit"
          class="start_game"
          form={formId}
          disabled={!(isEditable && can_start)}
        >
          Start game
        </button>
      </div>
    </>
  );
}
