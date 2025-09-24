import type { Call } from "../../../types/game";

import { Tile3D } from "../tile_3d/tile_3d";

import "./table_calls.css";

function TableCall({ call }: { call: Call }) {
  return (
    <span class="call">
      {call.tiles.map((tile) => (
        <Tile3D tile={tile} />
      ))}
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
        <TableCall call={call} />
      ))}
    </div>
  );
}
