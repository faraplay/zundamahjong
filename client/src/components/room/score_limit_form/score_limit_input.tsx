import type { ScoreLimit } from "../../../types/game_options";

export function GameOptionsScoreLimitInput({
  isEditable,
  index,
  scoreLimit,
  formId,
  removeThis,
  sendGameOptions,
}: {
  isEditable: boolean;
  index: number;
  scoreLimit: ScoreLimit;
  formId: string;
  removeThis: () => void;
  sendGameOptions: () => void;
}) {
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const editableProps = isEditable ? { onChange } : { readonly: true };
  return (
    <>
      <input
        form={formId}
        name={`${index}___han`}
        type="number"
        value={scoreLimit.han}
        {...editableProps}
      />
      <label>han:</label>
      <input
        form={formId}
        name={`${index}___score`}
        type="number"
        value={scoreLimit.score}
        {...editableProps}
      />
      {isEditable ? (
        <button class="remove_score_limit" type="button" onClick={removeThis}>
          &times;
        </button>
      ) : null}
    </>
  );
}
