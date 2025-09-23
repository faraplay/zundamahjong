import type { AllInfo } from "../../../types/game";

import { CenterInfo } from "../center_info/center_info";

import "./table.css";

export function Table({ info }: { info: AllInfo }) {
  return (
    <div id="table">
      <CenterInfo
        game_info={info.game_info}
        tiles_left={info.round_info.tiles_left}
        current_player={info.round_info.current_player}
      />
    </div>
  );
}
