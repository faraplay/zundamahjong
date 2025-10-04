import { useContext, useId } from "preact/hooks";

import { type GameOptions, type YakuValues } from "../../../types/game_options";

import { Emitter } from "../../emitter/emitter";
import { inputProps } from "../input_props";
import {
  GameOptionsNumberInput,
  GameOptionsCheckboxInput,
} from "../game_options_input/game_options_input";
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
    for (const prop of inputProps) {
      if (prop.type == "checkbox") {
        formData.set(
          prop.fieldName,
          formData.has(prop.fieldName) ? "True" : "False",
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
        {inputProps.map((props) =>
          props.type == "number" ? (
            <GameOptionsNumberInput
              key={props.fieldName}
              isEditable={isEditable}
              props={props}
              value={gameOptions[props.fieldName]}
              formId={formId}
              sendGameOptions={sendGameOptions}
            />
          ) : (
            <GameOptionsCheckboxInput
              key={props.fieldName}
              isEditable={isEditable}
              props={props}
              checked={gameOptions[props.fieldName]}
              formId={formId}
              sendGameOptions={sendGameOptions}
            />
          ),
        )}
        <YakuForm
          yakuValues={gameOptions.yaku_values}
          yakuFormId={yakuFormId}
          isEditable={isEditable}
          sendGameOptions={sendGameOptions}
        />
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
