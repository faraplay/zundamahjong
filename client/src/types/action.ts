import type { TileId } from "./tile";

export const enum ActionType {
  PASS = 0,
  CONTINUE = 1,
  DRAW = 2,
  DISCARD = 3,
  CHI_A = 4,
  CHI_B = 5,
  CHI_C = 6,
  PON = 7,
  OPEN_KAN = 8,
  ADD_KAN = 9,
  CLOSED_KAN = 10,
  FLOWER = 11,
  RON = 12,
  TSUMO = 13,
}

export type Action = {
  action_type: ActionType;
  tile: TileId;
};

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
