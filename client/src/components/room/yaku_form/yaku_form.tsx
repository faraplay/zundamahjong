import {
  type PatternValues,
  patterns,
  patternDisplayNames,
} from "../../../types/game_options";
import { GameOptionsNumberInput } from "../game_options_input/game_options_input";

export function PatternForm({
  patternValues,
  patternFormId,
  isEditable,
  sendGameOptions,
}: {
  patternValues: PatternValues;
  patternFormId: string;
  isEditable: boolean;
  sendGameOptions: () => void;
}) {
  return (
    <>
      {patterns.map((pattern) => (
        <GameOptionsNumberInput
          key={pattern}
          isEditable={isEditable}
          inputProps={{
            name: pattern,
            labelText: patternDisplayNames[pattern],
            type: "number",
          }}
          value={patternValues[pattern]}
          formId={patternFormId}
          sendGameOptions={sendGameOptions}
        />
      ))}
    </>
  );
}
