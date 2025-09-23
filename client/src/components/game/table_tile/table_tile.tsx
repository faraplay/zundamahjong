import type { TileId } from "../../../types/tile";

import { TileImage } from "../tile_image/tile_image";

import "./table_tile.css";

export function TableTile({ tile }: { tile: TileId }) {
  return (
    <div key={tile} class={`tile_div tile_id_${tile}`}>
      <span class="tile_face tile_back" />
      <span class="tile_face tile_left" />
      <span class="tile_face tile_right" />
      <span class="tile_face tile_top" />
      <span class="tile_face tile_bottom" />
      <span class="tile_face tile_front">
        <TileImage tile={tile} />
      </span>
    </div>
  );
}
