import { useContext, useLayoutEffect } from "preact/hooks";

import type { Player } from "../../../types/player";
import type { AvatarIdDict } from "../../../types/avatars";
import type { Action } from "../../../types/action";
import { RoundStatus, type AllInfo } from "../../../types/game";

import { Emitter } from "../../emitter/emitter";
import { EmitAction } from "../emit_action/emit_action";

import { PlayerIcons } from "../player_icon/player_icon";
import { Hand } from "../hand/hand";
import { ActionMenu } from "../action_menu/action_menu";
import { Table } from "../table/table";
import { WinInfo } from "../win_info/win_info";
import { Results } from "../results/results";

import { setAnimations } from "./animations";

import "./game_screen.css";
import { ShantenDisplayButton } from "../shanten_display/shanten_display";

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
      <WinInfo
        players={players}
        playerAvatarIds={playerAvatarIds}
        info={info}
        goToResults={goToResults}
      />
    ) : (
      <Results
        players={players}
        playerAvatarIds={playerAvatarIds}
        info={info}
      />
    );
  return (
    <EmitAction.Provider value={emit_action}>
      <div
        class={`game_screen me_player_${info.player_index} status_${info.round_info.status}`}
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
          <ActionMenu actions={info.player_info.actions} />
        )}
        {info.player_info.shanten_info ? (
          <ShantenDisplayButton shanten_info={info.player_info.shanten_info} />
        ) : (
          <></>
        )}
        <Table info={info} />
        {winOverlay}
      </div>
    </EmitAction.Provider>
  );
}
