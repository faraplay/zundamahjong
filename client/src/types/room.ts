import type { Player } from "./player";
import type { AvatarIdDict } from "./avatars";
import type { GameOptions } from "./game_options";

export type BasicRoom = {
  room_name: string;
  player_count: number;
  joined_players: Array<Player>;
};

export type DetailedRoom = BasicRoom & {
  avatars: AvatarIdDict;
  game_options: GameOptions;
};
