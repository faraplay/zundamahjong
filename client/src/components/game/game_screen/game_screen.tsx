import { useContext, useLayoutEffect } from "preact/hooks";

import type { Action } from "../../../types/action";
import { RoundStatus, type AllInfo } from "../../../types/game";

import { Emitter } from "../../emitter/emitter";

import { EmitAction } from "../emit_action/emit_action";
import { Hand } from "../hand/hand";
import { ActionMenu } from "../action_menu/action_menu";
import { Table } from "../table/table";
import { WinInfo } from "../win_info/win_info";
import { Results } from "../results/results";

import { setAnimations } from "./animations";
import { PlayerIcons } from "../player_icon/player_icon";
import type { AvatarIdDict } from "../../../types/avatars";
import type { Player } from "../../../types/player";

export function GameScreen({
  players,
  playerAvatarIds,
  info,
  actionSubmitted,
  setActionSubmitted,
  seeResults,
  goToResults,
}: {
  players: Player[];
  playerAvatarIds: AvatarIdDict;
  info: AllInfo;
  actionSubmitted: boolean;
  setActionSubmitted: () => void;
  seeResults: boolean;
  goToResults: () => void;
}) {
  const emit = useContext(Emitter);
  const emit_action = (action: Action) => {
    setActionSubmitted();
    emit("action", action, info.round_info.history.length);
  };
  useLayoutEffect(() => {
    setAnimations(info.history_updates);
  }, [info]);
  const winOverlay =
    info.round_info.status != RoundStatus.END ? (
      <></>
    ) : !seeResults ? (
      <WinInfo info={info} goToResults={goToResults} />
    ) : (
      <Results info={info} />
    );
  return (
    <EmitAction.Provider value={emit_action}>
      <div
        class={`me_player_${info.player_index} status_${info.round_info.status}`}
      >
        <PlayerIcons players={players} playerAvatarIds={playerAvatarIds} />
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
