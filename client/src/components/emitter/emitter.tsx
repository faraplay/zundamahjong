import { createContext } from "preact";

import type { EmitFunc } from "../../types/emit_func";

export const Emitter = createContext<EmitFunc>(() => {});
