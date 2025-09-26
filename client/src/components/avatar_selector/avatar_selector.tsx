import { useContext } from "preact/hooks";

import type { Player } from "../../types/player";
import { avatars, type AvatarIdDict } from "../../types/avatars";

import { Emitter } from "../emitter/emitter";

import "./avatar_selector.css";

export function AvatarSelector({
  player,
  canEdit,
  avatarId,
}: {
  player: Player;
  canEdit: boolean;
  avatarId: number;
}) {
  const emit = useContext(Emitter);
  const avatar = avatars[avatarId];
  const increaseAvatarId = (e: Event) => {
    e.preventDefault();
    emit("set_avatar", (avatarId + 1) % avatars.length);
  };
  const decreaseAvatarId = (e: Event) => {
    e.preventDefault();
    emit("set_avatar", (avatarId + avatars.length - 1) % avatars.length);
  };
  return (
    <div class="avatar_selector">
      <img
        class="avatar_selector_image"
        src={avatar.imageURL}
        alt={avatar.name}
      />
      <div class="avatar_selector_player_name">{player.name}</div>
      {canEdit ? (
        <>
          <button
            type="button"
            class="avatar_selector_decrease"
            onClick={decreaseAvatarId}
          >
            Prev
          </button>
          <button
            type="button"
            class="avatar_selector_increase"
            onClick={increaseAvatarId}
          >
            Next
          </button>
        </>
      ) : (
        <></>
      )}
    </div>
  );
}

export function AvatarDisplay({
  myPlayer,
  players,
  avatars,
}: {
  myPlayer: Player;
  players: ReadonlyArray<Player>;
  avatars: AvatarIdDict;
}) {
  return (
    <div class="avatar_display">
      {players.map((player) => (
        <AvatarSelector
          key={player.id}
          player={player}
          canEdit={player.id == myPlayer.id}
          avatarId={avatars[player.id]}
        />
      ))}
    </div>
  );
}
