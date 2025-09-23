import { getTileString, getTileUrl, type TileId } from "../../../types/tile";

import "./tile_image.css";

export function TileImage({ tile }: { tile: TileId }) {
  return (
    <img
      class="tile"
      src={getTileUrl(tile)}
      alt={getTileString(tile)}
      width={60}
      height={80}
    />
  );
}
