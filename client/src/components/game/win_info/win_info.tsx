import { avatars, type AvatarIdDict } from "../../../types/avatars";
import type { Player } from "../../../types/player";
import type { AllServerInfo } from "../../../types/game";

import { WinHand } from "../win_hand/win_hand";
import { YakuInfo } from "../yaku_info/yaku_info";
import { WinTotalScore } from "../win_total_score/win_total_score";

import "./win_info.css";

export function WinInfo({
  players,
  playerAvatarIds,
  info,
  goToResults,
}: {
  players: ReadonlyArray<Player>;
  playerAvatarIds: AvatarIdDict;
  info: AllServerInfo;
  goToResults: () => void;
}) {
  let winInfoInner = <></>;
  if (info.scoring_info) {
    const winnerAvatar =
      avatars[playerAvatarIds[players[info.scoring_info.win_player].id]];
    winInfoInner = (
      <>
        <img
          class="avatar"
          src={winnerAvatar.imageURL}
          alt={winnerAvatar.name}
        />
        <div id="yakus">
          {Object.entries(info.scoring_info.yaku_hans).map(([yaku, han]) => (
            <YakuInfo key={yaku} yaku={yaku} han={han} />
          ))}
        </div>
      </>
    );
  }
  return (
    <div id="win_info">
      <WinHand win_info={info.win_info} />
      {winInfoInner}
      <WinTotalScore
        win_player_name={
          info.scoring_info
            ? info.game_info.players[info.scoring_info.win_player].name
            : ""
        }
        scoring_info={info.scoring_info}
        goToResults={goToResults}
      />
    </div>
  );
}
