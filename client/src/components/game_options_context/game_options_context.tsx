import { createContext } from "preact";

import type { GameOptions } from "../../types/game_options";

export const GameOptionsContext = createContext<GameOptions | undefined>(
  undefined,
);
