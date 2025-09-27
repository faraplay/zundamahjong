import type { Player } from "./player";
import type { AvatarIdDict } from "./avatars";

export type Room = {
  room_name: string;
  player_count: number;
  joined_players: Array<Player>;
};

export type AvatarRoom = Room & {
  avatars: AvatarIdDict;
};
