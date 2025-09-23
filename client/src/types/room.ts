import type { Player } from "./player";

export type Room = {
  room_name: string;
  player_count: number;
  joined_players: Array<Player>;
};
