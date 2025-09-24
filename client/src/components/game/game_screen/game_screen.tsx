import { useContext, useState } from "preact/hooks";

import type { Action } from "../../../types/action";
import { RoundStatus, type AllInfo } from "../../../types/game";

import { Emitter } from "../../emitter/emitter";

import { EmitAction } from "../emit_action/emit_action";
import { Hand } from "../hand/hand";
import { ActionMenu } from "../action_menu/action_menu";
import { Table } from "../table/table";
import { WinInfo } from "../win_info/win_info";
import { Results } from "../results/results";

export function GameScreen({
  info,
  actionSubmitted,
  setActionSubmitted,
}: {
  info: AllInfo;
  actionSubmitted: boolean;
  setActionSubmitted: (_: boolean) => void;
}) {
  const [seeResults, setSeeResults] = useState(false);
  const emit = useContext(Emitter);
  const emit_action = (action: Action) => {
    setActionSubmitted(true);
    emit("action", action, info.round_info.history.length);
  };
  const winOverlay =
    info.round_info.status != RoundStatus.END ? (
      <></>
    ) : !seeResults ? (
      <WinInfo info={info} goToResults={() => setSeeResults(true)} />
    ) : (
      <Results info={info} closeResults={() => setSeeResults(false)} />
    );
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
        {actionSubmitted ? (
          <></>
        ) : (
          <ActionMenu
            actions={info.player_info.actions}
            last_discard={info.player_info.last_tile}
          />
        )}
        <Table info={info} />
        {winOverlay}
      </div>
    </EmitAction.Provider>
  );
}
