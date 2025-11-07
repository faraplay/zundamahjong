import { useContext } from "preact/hooks";
import { type Action, type HandTileActionType } from "../../../types/action";
import type { TileId } from "../../../types/tile";

import { Tile2D } from "../tile_2d/tile_2d";

import "./hand.css";
import { EmitAction } from "../emit_action/emit_action";

function HandTile({
  action_type,
  tile,
  canDoAction,
  setHoverTile,
}: {
  action_type: HandTileActionType;
  tile: TileId;
  canDoAction: boolean;
  setHoverTile: (tile: TileId | null) => void;
}) {
  const action: Action = { action_type, tile };
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
      disabled={!canDoAction}
      onClick={submitAction}
      onMouseEnter={startHoverAction}
      onMouseLeave={endHoverAction}
    >
      <Tile2D tile={tile} />
    </button>
  );
}

export function Hand({
  handActionType,
  tiles,
  actions,
  actionSubmitted,
  setHoverTile,
}: {
  handActionType: HandTileActionType;
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
          action_type={handActionType}
          tile={tile}
          canDoAction={
            !actionSubmitted &&
            actions.some(
              (action) =>
                action.action_type == handActionType && action.tile == tile,
            )
          }
          setHoverTile={setHoverTile}
        />
      ))}
    </div>
  );
}
