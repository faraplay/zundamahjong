import { createContext } from "preact";

import type { GameOptions } from "../../types/game_options";
import type { ClientOptions } from "../../types/client_options";

type Options = {
  client_options: ClientOptions;
  set_client_options: (value: ClientOptions) => void;
  game_options: GameOptions;
};

export const OptionsContext = createContext<Options | undefined>(undefined);
