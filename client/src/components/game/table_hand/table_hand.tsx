import type { TileId } from "../../../types/tile";
import { Tile3D } from "../tile_3d/tile_3d";

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
        {tiles.map((tile, index) => (
          <Tile3D key={index} tile={tile} />
        ))}
      </div>
    </div>
  );
}
