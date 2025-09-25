import type { AllInfo } from "../../../types/game";

import { WinHand } from "../win_hand/win_hand";
import { YakuInfo } from "../yaku_info/yaku_info";
import { WinTotalScore } from "../win_total_score/win_total_score";

import "./win_info.css";

export function WinInfo({
  info,
  goToResults,
}: {
  info: AllInfo;
  goToResults: () => void;
}) {
  return (
    <div id="win_info">
      <WinHand win_info={info.win_info} />
      {info.scoring_info ? (
        <>
          <div id="yakus">
            {Object.entries(info.scoring_info.yaku_hans).map(([yaku, han]) => (
              <YakuInfo key={yaku} yaku={yaku} han={han} />
            ))}
          </div>
        </>
      ) : (
        <></>
      )}
      <WinTotalScore
        win_player_name={
          info.scoring_info
            ? info.game_info.player_names[info.scoring_info.win_player]
            : ""
        }
        scoring_info={info.scoring_info}
        goToResults={goToResults}
      />
    </div>
  );
}
