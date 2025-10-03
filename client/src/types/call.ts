import type { TileId } from "./tile";

export const enum CallType {
  CHI = 0,
  PON = 1,
  OPEN_KAN = 2,
  ADD_KAN = 3,
  CLOSED_KAN = 4,
}

export type OpenCall = {
  call_type: CallType.CHI | CallType.PON;
  called_player_index: number;
  called_tile: TileId;
  other_tiles: [TileId, TileId];
};

export type OpenKanCall = {
  call_type: CallType.OPEN_KAN;
  called_player_index: number;
  called_tile: TileId;
  other_tiles: [TileId, TileId, TileId];
};

export type AddKanCall = {
  call_type: CallType.ADD_KAN;
  called_player_index: number;
  called_tile: TileId;
  added_tile: TileId;
  other_tiles: [TileId, TileId];
};

export type ClosedKanCall = {
  call_type: CallType.CLOSED_KAN;
  tiles: [TileId, TileId, TileId, TileId];
};

export type Call = OpenCall | OpenKanCall | AddKanCall | ClosedKanCall;

export function getCallTiles(call: Call) {
  if (call.call_type == CallType.CLOSED_KAN) {
    return call.tiles;
  }
  if (call.call_type == CallType.ADD_KAN) {
    return [call.added_tile, call.called_tile, ...call.other_tiles];
  }
  return [call.called_tile, ...call.other_tiles].sort();
}
