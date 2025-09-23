import type { AllInfo } from "../../../types/game";

import { Table } from "../table/table";

export function GameScreen({ info }: { info: AllInfo }) {
  return (
    <div
      class={`me_player_${info.player_index} status_${info.round_info.status}`}
    >
      <Table info={info} />
    </div>
  );
}
