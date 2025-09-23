import type { AllInfo } from "../../../types/game";
import { Hand } from "../hand/hand";

import { Table } from "../table/table";

export function GameScreen({ info }: { info: AllInfo }) {
  return (
    <div
      class={`me_player_${info.player_index} status_${info.round_info.status}`}
    >
      <Hand tiles={info.player_info.hand} actions={info.player_info.actions} />
      <Table info={info} />
    </div>
  );
}
