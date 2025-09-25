import { createContext } from "preact";
import type { Action } from "../../../types/action";

export const EmitAction = createContext<(action: Action) => void>(() => {});
