import { ActionType, type Action } from "../../../types/action";

import { Tile2D } from "../tile_2d/tile_2d";

import "./action_disambig_menu.css";
import { useContext } from "preact/hooks";
import { EmitAction } from "../emit_action/emit_action";

function ActionDisambigMenuItem({
  action,
  unsetDisambig,
}: {
  action: Action;
  unsetDisambig: () => void;
}) {
  const emit_action = useContext(EmitAction);
  const onClick = (e: Event) => {
    e.preventDefault();
    unsetDisambig();
    emit_action(action);
  };
  return (
    <button type="button" class="disambig_action_button" onClick={onClick}>
      {(function () {
        switch (action.action_type) {
          case ActionType.CHII:
          case ActionType.PON:
            return action.other_tiles.map((tile) => (
              <Tile2D key={tile} tile={tile} />
            ));
          case ActionType.CLOSED_KAN:
            return <Tile2D tile={action.tiles[0]} />;
          case ActionType.ADD_KAN:
          case ActionType.FLOWER:
            return <Tile2D tile={action.tile} />;
          default:
            return <></>;
        }
      })()}
    </button>
  );
}

export function ActionDisambigMenu({
  disambigActions,
  unsetDisambig,
}: {
  disambigActions: ReadonlyArray<Action>;
  unsetDisambig: () => void;
}) {
  return (
    <div class="disambig_div">
      <div class="disambig_text">Select an option</div>
      {disambigActions.map((action) => (
        <ActionDisambigMenuItem
          key={action}
          action={action}
          unsetDisambig={unsetDisambig}
        />
      ))}
    </div>
  );
}
