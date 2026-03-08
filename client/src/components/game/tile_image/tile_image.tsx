import { getTileShortString, getTileString, getTileUrl, type TileId } from "../../../types/tile";

import "./tile_image.css";

export function TileImage({ tile }: { tile: TileId }) {
  return (
    <div class="tile_image" data-shortname={getTileShortString(tile)}>
      <img
        src={getTileUrl(tile)}
        alt={getTileString(tile)}
        width={60}
        height={80}
      />
    </div>
  );
}
