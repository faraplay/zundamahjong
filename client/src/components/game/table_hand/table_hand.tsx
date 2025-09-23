import type { TileId } from "../../../types/tile";
import { TableTile } from "../table_tile/table_tile";

import "./table_hand.css";

export function TableHand({
  player_index,
  tiles,
}: {
  player_index: number;
  tiles: ReadonlyArray<TileId>;
}) {
  return (
    <div class={`table_hand_outer player_${player_index}`}>
      <div class="table_hand">
        {tiles.map((tile) => (
          <TableTile tile={tile} />
        ))}
      </div>
    </div>
  );
}
