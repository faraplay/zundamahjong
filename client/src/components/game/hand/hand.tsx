import { useContext } from "preact/hooks";
import { ActionType, type Action } from "../../../types/game";
import type { TileId } from "../../../types/tile";

import { Tile2D } from "../tile_2d/tile_2d";

import "./hand.css";
import { EmitAction } from "../emit_action/emit_action";

function HandTile({ tile, canDiscard }: { tile: TileId; canDiscard: boolean }) {
  const action: Action = {
    action_type: ActionType.DISCARD,
    tile: tile,
  };
  const emit_action = useContext(EmitAction);
  const submitAction = (e: Event) => {
    e.preventDefault();
    emit_action(action);
  };
  return (
    <button
      key={tile}
      type="button"
      class="hand_tile_button"
      disabled={!canDiscard}
      onClick={submitAction}
    >
      <Tile2D tile={tile} />
    </button>
  );
}

export function Hand({
  tiles,
  actions,
  actionSubmitted,
}: {
  tiles: ReadonlyArray<TileId>;
  actions: ReadonlyArray<Action>;
  actionSubmitted: boolean;
}) {
  return (
    <div id="hand">
      {tiles.map((tile) => (
        <HandTile
          tile={tile}
          canDiscard={
            !actionSubmitted &&
            actions.some(
              (action) =>
                action.action_type == ActionType.DISCARD && action.tile == tile,
            )
          }
        />
      ))}
    </div>
  );
}
