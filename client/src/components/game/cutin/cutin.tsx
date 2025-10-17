import {
  getActionSupertype,
  getActionSupertypeString,
  isCutinAction,
  type ActionSupertype,
} from "../../../types/action";
import { avatars } from "../../../types/avatars";
import type { HistoryItem } from "../../../types/game";

import "./cutin.css";

export function Cutin({
  actionSupertype,
  playerIndex,
  avatarId,
}: {
  actionSupertype: ActionSupertype;
  playerIndex: number;
  avatarId: number;
}) {
  const avatar = avatars[avatarId];
  const supertypeString = getActionSupertypeString(actionSupertype);
  return (
    <div class={`cutin action_${actionSupertype} player_${playerIndex}`}>
      <img class="avatar" src={avatar.imageURL} alt={avatar.name} />
      <div
        class={`cutin_highlight action_${actionSupertype}`}
        data-text={supertypeString}
      >
        <div class="cutin_text">{supertypeString}</div>
      </div>
    </div>
  );
}

export function CutinCollection({
  historyUpdates,
  avatarIds,
}: {
  historyUpdates: HistoryItem[];
  avatarIds: number[];
}) {
  const playerActionSupertypes = historyUpdates
    .filter((historyItem) => isCutinAction(historyItem.action.action_type))
    .map((historyItem) => {
      return {
        supertype: getActionSupertype(historyItem.action.action_type),
        playerIndex: historyItem.player_index,
      };
    });
  const playerActionSupertypesDict: {
    [key: string]: { supertype: ActionSupertype; playerIndex: number };
  } = {};
  for (const obj of playerActionSupertypes) {
    playerActionSupertypesDict[
      `action_${obj.supertype} player_${obj.playerIndex}`
    ] = obj;
  }
  return (
    <div class="cutins">
      {Object.entries(playerActionSupertypesDict).map(
        ([key, { supertype, playerIndex }]) => (
          <Cutin
            key={key}
            actionSupertype={supertype}
            playerIndex={playerIndex}
            avatarId={avatarIds[playerIndex]}
          />
        ),
      )}
    </div>
  );
}
