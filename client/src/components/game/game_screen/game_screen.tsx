import { useContext } from "preact/hooks";

import type { Action, AllInfo } from "../../../types/game";

import { Emitter } from "../../emitter/emitter";

import { EmitAction } from "../emit_action/emit_action";
import { Hand } from "../hand/hand";
import { Table } from "../table/table";

export function GameScreen({
  info,
  actionSubmitted,
  setActionSubmitted,
}: {
  info: AllInfo;
  actionSubmitted: boolean;
  setActionSubmitted: (_: boolean) => void;
}) {
  const emit = useContext(Emitter);
  const emit_action = (action: Action) => {
    setActionSubmitted(true);
    emit("action", action, info.round_info.history.length);
  };
  return (
    <EmitAction.Provider value={emit_action}>
      <div
        class={`me_player_${info.player_index} status_${info.round_info.status}`}
      >
        <Hand
          tiles={info.player_info.hand}
          actions={info.player_info.actions}
          actionSubmitted={actionSubmitted}
        />
        <Table info={info} />
      </div>
    </EmitAction.Provider>
  );
}
