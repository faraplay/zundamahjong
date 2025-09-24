import type { TileId } from "../../../types/tile";

import { Tile3D } from "../tile_3d/tile_3d";

import "./table_discards.css";

export function TableDiscards({
  player_index,
  tiles,
}: {
  player_index: number;
  tiles: ReadonlyArray<TileId>;
}) {
  return (
    <div class={`player_discards player_${player_index}`}>
      {tiles.map((tile) => (
        <Tile3D tile={tile} />
      ))}
    </div>
  );
}
