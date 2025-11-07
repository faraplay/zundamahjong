import { useContext, useEffect, useLayoutEffect, useState } from "preact/hooks";

import type { AvatarIdDict } from "../../../types/avatars";
import {
  ActionType,
  type Action,
  type HandTileActionType,
} from "../../../types/action";
import { RoundStatus } from "../../../types/game";
import { type AllInfo } from "../../../process_info";

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
import {
  ShantenDisplay,
  ShantenDisplayButton,
} from "../shanten_display/shanten_display";
import { type TileId } from "../../../types/tile";
import { VoiceCollection } from "../../audio_collection/audio_collection";
import { CutinCollection } from "../cutin/cutin";

export function GameScreen({
  playerAvatarIds,
  info,
  actionSubmitted,
  setActionSubmitted,
  seeResults,
  goToResults,
}: {
  playerAvatarIds: AvatarIdDict;
  info: AllInfo;
  actionSubmitted: boolean;
  setActionSubmitted: () => void;
  seeResults: boolean;
  goToResults: () => void;
}) {
  const [hoverTile, setHoverTile] = useState<TileId | null>(null);
  const [handActionType, setHandActionType] = useState<HandTileActionType>(
    ActionType.DISCARD,
  );

  const emit = useContext(Emitter);
  const emit_action = (action: Action) => {
    setActionSubmitted();
    emit("action", action, info.round_info.history.length);
  };

  useEffect(() => {
    if (info.round_info.current_player == info.player_index) {
      if (info.round_info.status == RoundStatus.START) {
        setHandActionType(ActionType.FLOWER);
      } else {
        setHandActionType(ActionType.DISCARD);
      }
    } else {
      setHandActionType(ActionType.DISCARD);
    }
  }, [info]);

  useLayoutEffect(() => {
    // calculate this inside to avoid triggering this effect every time
    // this component is rerendered
    const avatarIds = info.game_info.players.map(
      (player) => playerAvatarIds[player.id],
    );
    setAnimations(info.history_updates, avatarIds);
  }, [info, playerAvatarIds]);

  const avatarIds = info.game_info.players.map(
    (player) => playerAvatarIds[player.id],
  );
  const voiceCollections = [...new Set(Object.values(playerAvatarIds))].map(
    (avatarId) => <VoiceCollection key={avatarId} avatarId={avatarId} />,
  );

  const winOverlay =
    info.round_info.status != RoundStatus.END ? (
      <></>
    ) : !seeResults ? (
      <WinInfo
        players={info.game_info.players}
        playerAvatarIds={playerAvatarIds}
        info={info}
        goToResults={goToResults}
      />
    ) : (
      <Results
        players={info.game_info.players}
        playerAvatarIds={playerAvatarIds}
        info={info}
      />
    );

  const discard_shanten_info =
    info.player_info.discard_shanten_info &&
    hoverTile &&
    info.player_info.discard_shanten_info[hoverTile];

  return (
    <EmitAction.Provider value={emit_action}>
      <div
        class={`game_screen me_player_${info.player_index} status_${info.round_info.status}`}
      >
        {voiceCollections}
        <CutinCollection
          historyUpdates={info.history_updates}
          avatarIds={avatarIds}
        />
        <PlayerIcons
          players={info.game_info.players}
          playerAvatarIds={playerAvatarIds}
        />
        <Hand
          handActionType={handActionType}
          tiles={info.player_info.hand}
          actions={info.player_info.actions}
          actionSubmitted={actionSubmitted}
          setHoverTile={setHoverTile}
        />
        {actionSubmitted ? (
          <></>
        ) : (
          <ActionMenu
            actions={info.player_info.actions}
            handActionType={handActionType}
            setHandActionType={setHandActionType}
          />
        )}
        {info.player_info.shanten_info ? (
          <ShantenDisplayButton
            shantenInfo={info.player_info.shanten_info}
            remainingTileCounts={info.player_info.remaining_tile_counts}
          />
        ) : (
          <></>
        )}
        {discard_shanten_info ? (
          <ShantenDisplay
            shantenInfo={discard_shanten_info}
            remainingTileCounts={info.player_info.remaining_tile_counts}
            visible
          />
        ) : (
          <></>
        )}
        <Table info={info} />
        {winOverlay}
      </div>
    </EmitAction.Provider>
  );
}
