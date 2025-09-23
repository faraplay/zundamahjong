import { createContext } from "preact";
import type { Action } from "../../../types/game";

export const EmitAction = createContext((_: Action) => {});
