import { avatars, type AvatarIdDict } from "../../../types/avatars";
import type { Player } from "../../../types/player";
import "./player_icon.css";

function PlayerIcon({
  player_index,
  player_name,
  playerAvatarId,
}: {
  player_index: number;
  player_name: string;
  playerAvatarId: number;
}) {
  return (
    <div class={`player_icon player_${player_index}`}>
      <img
        class="player_icon_image"
        src={avatars[playerAvatarId].faceURL}
        alt={avatars[playerAvatarId].name}
      />
      <div class="player_icon_name">{player_name}</div>
    </div>
  );
}

export function PlayerIcons({
  players,
  playerAvatarIds,
}: {
  players: Player[];
  playerAvatarIds: AvatarIdDict;
}) {
  return (
    <div id="player_names">
      {players.map((player, index) => (
        <PlayerIcon
          key={index}
          player_index={index}
          player_name={player.name}
          playerAvatarId={playerAvatarIds[player.id]}
        />
      ))}
    </div>
  );
}
