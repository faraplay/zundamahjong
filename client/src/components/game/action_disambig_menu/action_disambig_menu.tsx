import type { TileId } from "../../../types/tile";
import {
  ActionType,
  type Action,
  type ActionSupertype,
} from "../../../types/action";

import { Tile2D } from "../tile_2d/tile_2d";

import "./action_disambig_menu.css";
import { useContext } from "preact/hooks";
import { EmitAction } from "../emit_action/emit_action";

function ActionDisambigMenuItem({
  action,
  last_discard,
  setActionDisambigMenuProps,
}: {
  action: Action;
  last_discard: TileId;
  setActionDisambigMenuProps: (value: ActionDisambigMenuProps | null) => void;
}) {
  const emit_action = useContext(EmitAction);
  const onClick = (e: Event) => {
    e.preventDefault();
    setActionDisambigMenuProps(null);
    emit_action(action);
  };
  return (
    <button type="button" class="disambig_action_button" onClick={onClick}>
      {(function () {
        switch (action.action_type) {
          case ActionType.CHI_A:
            return [last_discard, last_discard + 4, last_discard + 8].map(
              (tile) => <Tile2D tile={tile as TileId} />,
            );
          case ActionType.CHI_B:
            return [last_discard - 4, last_discard, last_discard + 4].map(
              (tile) => <Tile2D tile={tile as TileId} />,
            );
          case ActionType.CHI_C:
            return [last_discard - 8, last_discard - 4, last_discard].map(
              (tile) => <Tile2D tile={tile as TileId} />,
            );
          case ActionType.ADD_KAN:
          case ActionType.CLOSED_KAN:
          case ActionType.FLOWER:
            return <Tile2D tile={action.tile} />;
          default:
            return <></>;
        }
      })()}
    </button>
  );
}

export type ActionDisambigMenuProps = {
  action_supertype: ActionSupertype;
  actions: ReadonlyArray<Action>;
  last_discard: TileId;
};

export function ActionDisambigMenu({
  props,
  setActionDisambigMenuProps,
}: {
  props: ActionDisambigMenuProps;
  setActionDisambigMenuProps: (value: ActionDisambigMenuProps | null) => void;
}) {
  const { action_supertype, actions, last_discard } = props;
  const sorted_actions =
    action_supertype == 1
      ? [...actions].sort((a, b) => b.action_type - a.action_type)
      : [...actions].sort((a, b) => a.tile - b.tile);
  return (
    <div class="disambig_div">
      <div class="disambig_text">Select an option</div>
      {sorted_actions.map((action) => (
        <ActionDisambigMenuItem
          action={action}
          last_discard={last_discard}
          setActionDisambigMenuProps={setActionDisambigMenuProps}
        />
      ))}
    </div>
  );
}
