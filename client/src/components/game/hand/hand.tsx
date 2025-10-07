import { useContext } from "preact/hooks";
import { ActionType, type Action } from "../../../types/action";
import type { TileId } from "../../../types/tile";

import { Tile2D } from "../tile_2d/tile_2d";

import "./hand.css";
import { EmitAction } from "../emit_action/emit_action";

function HandTile({
  tile,
  canDiscard,
  setHoverTile,
}: {
  tile: TileId;
  canDiscard: boolean;
  setHoverTile: (tile: TileId | null) => void;
}) {
  const action: Action = {
    action_type: ActionType.DISCARD,
    tile,
  };
  const emit_action = useContext(EmitAction);
  const submitAction = (e: Event) => {
    e.preventDefault();
    emit_action(action);
  };
  const startHoverAction = (e: Event) => {
    e.preventDefault();
    setHoverTile(tile);
  };
  const endHoverAction = (e: Event) => {
    e.preventDefault();
    setHoverTile(null);
  };
  return (
    <button
      key={tile}
      type="button"
      class="hand_tile_button"
      disabled={!canDiscard}
      onClick={submitAction}
      onMouseEnter={startHoverAction}
      onMouseLeave={endHoverAction}
    >
      <Tile2D tile={tile} />
    </button>
  );
}

export function Hand({
  tiles,
  actions,
  actionSubmitted,
  setHoverTile,
}: {
  tiles: ReadonlyArray<TileId>;
  actions: ReadonlyArray<Action>;
  actionSubmitted: boolean;
  setHoverTile: (tile: TileId | null) => void;
}) {
  return (
    <div id="hand">
      {tiles.map((tile) => (
        <HandTile
          key={tile}
          tile={tile}
          canDiscard={
            !actionSubmitted &&
            actions.some(
              (action) =>
                action.action_type == ActionType.DISCARD && action.tile == tile,
            )
          }
          setHoverTile={setHoverTile}
        />
      ))}
    </div>
  );
}
