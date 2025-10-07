import type { TileId, TileValue } from "./tile.ts";
import type { Call } from "./call.ts";
import type { Action } from "./action.ts";

export type Discard = {
  player: number;
  tile: TileId;
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
  player_names: string[];
  wind_round: number;
  sub_round: number;
  draw_count: number;
  player_scores: number[];
};

export type RoundInfo = {
  tiles_left: number;
  current_player: number;
  status: RoundStatus;
  hand_counts: number[];
  discards: Discard[];
  calls: Call[][];
  flowers: TileId[][];
  history: HistoryItem[];
};

export type PlayerInfo = {
  hand: TileId[];
  last_tile: TileId;
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
  yaku_hans: { [yaku: string]: number };
  han_total: number;
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

export type AllInfo = AllServerInfo & {
  player_info: {
    shanten_info?: [number, Set<TileValue>];
    discard_shanten_info?: { [tile in TileId]?: [number, Set<TileValue>] };
  };
};
