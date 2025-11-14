import {
  type PatternDataDict,
  patternDisplayNames,
  patterns,
} from "../../../types/game_options";
import { GameOptionsPatternInput } from "./pattern_input";

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

export function getPatternDataDict(patternFormId: string): PatternDataDict {
  const patternFormData = new FormData(
    document.getElementById(patternFormId) as HTMLFormElement,
  );
  return Object.fromEntries(
    patterns.map((pattern) => [
      pattern,
      {
        display_name: patternDisplayNames[pattern],
        han: Number(patternFormData.get(`${pattern}___han`)),
        fu: Number(patternFormData.get(`${pattern}___fu`)),
      },
    ]),
  ) as PatternDataDict;
}
