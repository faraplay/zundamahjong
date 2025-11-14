import type { ScoreLimit } from "../../../types/game_options";
import { GameOptionsScoreLimitInput } from "./score_limit_input";

import "./score_limit_form.css";

export function ScoreLimitForm({
  scoreLimits,
  scoreLimitFormId,
  isEditable,
  addNewScoreLimit,
  removeScoreLimit,
  sendGameOptions,
  onSubmit,
}: {
  scoreLimits: ScoreLimit[];
  scoreLimitFormId: string;
  isEditable: boolean;
  addNewScoreLimit: () => void;
  removeScoreLimit: (index: number) => void;
  sendGameOptions: () => void;
  onSubmit: (e: SubmitEvent) => void;
}) {
  return (
    <>
      <form
        id={scoreLimitFormId}
        data-count={scoreLimits.length}
        onSubmit={onSubmit}
        hidden
      />
      {scoreLimits.map((scoreLimit, index) => (
        <GameOptionsScoreLimitInput
          key={scoreLimit}
          isEditable={isEditable}
          index={index}
          scoreLimit={scoreLimit}
          formId={scoreLimitFormId}
          removeThis={() => {
            removeScoreLimit(index);
          }}
          sendGameOptions={sendGameOptions}
        />
      ))}
      {isEditable ? (
        <button
          class="add_new_score_limit"
          type="button"
          onClick={addNewScoreLimit}
        >
          Add new score limit...
        </button>
      ) : null}
    </>
  );
}

export function getScoreLimits(scoreLimitFormId: string): ScoreLimit[] {
  const scoreLimitForm = document.getElementById(
    scoreLimitFormId,
  ) as HTMLFormElement;
  const scoreLimitFormData = new FormData(scoreLimitForm);
  const scoreLimitCount = Number(scoreLimitForm.dataset["count"]);
  const scoreLimits: ScoreLimit[] = [];
  for (let index = 0; index < scoreLimitCount; index++) {
    scoreLimits.push({
      han: Number(scoreLimitFormData.get(`${index}___han`)),
      score: Number(scoreLimitFormData.get(`${index}___score`)),
    });
  }
  return scoreLimits;
}
