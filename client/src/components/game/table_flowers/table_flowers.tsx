import type { TileId } from "../../../types/tile";

import { Tile3DList } from "../tile_3d/tile_3d";

import "./table_flowers.css";

export function TableFlowers({
  player_index,
  tiles,
}: {
  player_index: number;
  tiles: ReadonlyArray<TileId>;
}) {
  return (
    <div class={`player_flowers player_${player_index}`}>
      <Tile3DList tiles={tiles} />
    </div>
  );
}
