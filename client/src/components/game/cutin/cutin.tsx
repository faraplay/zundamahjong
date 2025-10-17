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
  const uniquePlayerActionSupertypes = [...new Set(playerActionSupertypes)];
  return (
    <div class="cutins">
      {uniquePlayerActionSupertypes.map(({ supertype, playerIndex }) => (
        <Cutin
          key={`action_${supertype} player_${playerIndex}`}
          actionSupertype={supertype}
          playerIndex={playerIndex}
          avatarId={avatarIds[playerIndex]}
        />
      ))}
    </div>
  );
}
