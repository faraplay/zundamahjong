import type { TileId } from "../../../types/tile";

import { TileImage } from "../tile_image/tile_image";

import "./tile_2d.css";

export function Tile2D({ tile }: { tile: TileId }) {
  return (
    <span class="tile_div tile_2d tile_2d_front">
      <div class="tile_back_layer" />
      <div class="tile_middle_layer" />
      <TileImage tile={tile} />
    </span>
  );
}

export function Tile2DBack() {
  return (
    <span class="tile_div tile_2d tile_2d_back">
      <div class="tile_back_layer" />
      <div class="tile_middle_layer" />
      <div class="tile_front_layer" />
    </span>
  );
}

export function Tile2DList({ tiles }: { tiles: ReadonlyArray<TileId> }) {
  return (
    <>
      {tiles.map((tile) => (
        <Tile2D key={tile} tile={tile} />
      ))}
    </>
  );
}
