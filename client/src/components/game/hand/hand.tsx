import { ActionType, type Action } from "../../../types/game";
import type { TileId } from "../../../types/tile";

import { Tile2D } from "../tile_2d/tile_2d";

import "./hand.css";

function HandTile({ tile, isActive }: { tile: TileId; isActive: boolean }) {
  return (
    <button
      key={tile}
      type="button"
      class="hand_tile_button"
      disabled={!isActive}
    >
      <Tile2D tile={tile} />
    </button>
  );
}

export function Hand({
  tiles,
  actions,
}: {
  tiles: ReadonlyArray<TileId>;
  actions: ReadonlyArray<Action>;
}) {
  console.log(tiles, actions);
  return (
    <div id="hand">
      {tiles.map((tile) => (
        <HandTile
          tile={tile}
          isActive={actions.some(
            (action) =>
              action.action_type == ActionType.DISCARD && action.tile == tile,
          )}
        />
      ))}
    </div>
  );
}
