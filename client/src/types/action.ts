import type { CallType, OpenCall } from "./call";
import type { TileId } from "./tile";

export const enum ActionType {
  PASS = 0,
  CONTINUE = 1,
  DRAW = 2,
  DISCARD = 3,
  CHII = 6,
  PON = 7,
  OPEN_KAN = 8,
  ADD_KAN = 9,
  CLOSED_KAN = 10,
  FLOWER = 11,
  RON = 12,
  TSUMO = 13,
}

export type SimpleAction = {
  action_type:
    | ActionType.PASS
    | ActionType.CONTINUE
    | ActionType.DRAW
    | ActionType.RON
    | ActionType.TSUMO;
};

export type HandTileAction = {
  action_type: ActionType.DISCARD | ActionType.FLOWER;
  tile: TileId;
};

export type OpenCallAction = {
  action_type: ActionType.CHII | ActionType.PON;
  other_tiles: [TileId, TileId];
};

export type OpenKanAction = {
  action_type: ActionType.OPEN_KAN;
  other_tiles: [TileId, TileId, TileId];
};

export type AddKanAction = {
  action_type: ActionType.ADD_KAN;
  tile: TileId;
  pon_call: OpenCall & { call_type: CallType.PON };
};

export type ClosedKanAction = {
  action_type: ActionType.CLOSED_KAN;
  tiles: [TileId, TileId, TileId, TileId];
};

export type Action =
  | SimpleAction
  | HandTileAction
  | OpenCallAction
  | OpenKanAction
  | AddKanAction
  | ClosedKanAction;

const action_supertypes = [7, 7, 7, 0, 1, 1, 1, 2, 3, 3, 3, 4, 5, 6] as const;

const action_supertype_strings = [
  "",
  "Chii",
  "Pon",
  "Kan",
  "Flower",
  "Ron",
  "Tsumo",
  "Pass",
] as const;

export type ActionSupertype = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;

export function getActionSupertype(action_type: ActionType) {
  return action_supertypes[action_type];
}

export function getActionSupertypeString(action_supertype: ActionSupertype) {
  return action_supertype_strings[action_supertype];
}

export function isCutinAction(action_type: ActionType) {
  return action_type > 3;
}
