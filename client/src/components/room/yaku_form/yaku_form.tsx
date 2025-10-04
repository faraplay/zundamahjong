import {
  type YakuValues,
  yakus,
  yakuDisplayNames,
} from "../../../types/game_options";
import { GameOptionsNumberInput } from "../game_options_input/game_options_input";

export function YakuForm({
  yakuValues,
  yakuFormId,
  isEditable,
  sendGameOptions,
}: {
  yakuValues: YakuValues;
  yakuFormId: string;
  isEditable: boolean;
  sendGameOptions: () => void;
}) {
  return (
    <>
      {yakus.map((yaku) => (
        <GameOptionsNumberInput
          key={yaku}
          isEditable={isEditable}
          props={{
            fieldName: yaku,
            labelText: yakuDisplayNames[yaku],
            type: "number",
          }}
          value={yakuValues[yaku]}
          formId={yakuFormId}
          sendGameOptions={sendGameOptions}
        />
      ))}
    </>
  );
}
