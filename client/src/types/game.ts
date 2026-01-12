import type { TileId } from "./tile.ts";
import type { Call } from "./call.ts";
import type { Action } from "./action.ts";
import type { Player } from "./player.ts";
import type { PatternData } from "./game_options.ts";

export type Discard = {
  player: number;
  tile: TileId;
  is_new: boolean;
  is_called: boolean;
  is_added_kan: boolean;
  is_closed_kan: boolean;
};

export type HistoryItem = {
  player_index: number;
  action: Action;
};

export const enum RoundStatus {
  START = 0,
  PLAY = 1,
  CALLED_PLAY = 2,
  ADD_KAN_AFTER = 3,
  CLOSED_KAN_AFTER = 4,
  DISCARDED = 5,
  LAST_DISCARDED = 6,
  END = 7,
}

export type GameInfo = {
  players: Player[];
  wind_round: number;
  sub_round: number;
  draw_count: number;
  player_scores: number[];
};

export type RoundInfo = {
  tiles_left: number;
  current_player: number;
  status: RoundStatus;
  discards: Discard[];
  history: HistoryItem[];
  hand_counts: number[];
  riichi_discard_indexes: (number | null)[];
  calls: Call[][];
  flowers: TileId[][];
};

export type PlayerInfo = {
  hand: TileId[];
  actions: Action[];
};

export type Win = {
  win_player: number;
  lose_player: number | null;
  hand: TileId[];
  calls: Call[];
  flowers: TileId[];
};

export type Scoring = {
  win_player: number;
  lose_player: number | null;
  patterns: { [pattern: string]: PatternData };
  han: number;
  fu: number;
  player_scores: number[];
};

export type AllServerInfo = {
  player_count: number;
  player_index: number;
  is_game_end: boolean;
  game_info: GameInfo;
  round_info: RoundInfo;
  history_updates: HistoryItem[];
  player_info: PlayerInfo;
  win_info: Win | null;
  scoring_info: Scoring | null;
};
