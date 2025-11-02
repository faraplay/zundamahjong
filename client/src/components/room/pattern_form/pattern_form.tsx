import { type PatternDataDict, patterns } from "../../../types/game_options";
import { GameOptionsPatternInput } from "../game_options_input/game_options_input";

export function PatternForm({
  patternValues,
  patternFormId,
  isEditable,
  sendGameOptions,
}: {
  patternValues: PatternDataDict;
  patternFormId: string;
  isEditable: boolean;
  sendGameOptions: () => void;
}) {
  return (
    <>
      {patterns.map((pattern) => (
        <GameOptionsPatternInput
          key={pattern}
          isEditable={isEditable}
          name={pattern}
          data={patternValues[pattern]}
          formId={patternFormId}
          sendGameOptions={sendGameOptions}
        />
      ))}
    </>
  );
}
