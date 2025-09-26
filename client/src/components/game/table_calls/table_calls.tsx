import type { Call } from "../../../types/game";

import { Tile3DList } from "../tile_3d/tile_3d";

import "./table_calls.css";

function TableCall({ call }: { call: Call }) {
  return (
    <span class="call">
      <Tile3DList tiles={call.tiles} />
    </span>
  );
}

export function TableCalls({
  player_index,
  calls,
}: {
  player_index: number;
  calls: ReadonlyArray<Call>;
}) {
  return (
    <div class={`player_calls player_${player_index}`}>
      {calls.map((call) => (
        <TableCall key={call} call={call} />
      ))}
    </div>
  );
}
