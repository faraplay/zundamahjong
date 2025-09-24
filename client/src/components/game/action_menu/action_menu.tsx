import { useContext, useState } from "preact/hooks";
import {
  type Action,
  type ActionSupertype,
  getActionSupertype,
  getActionSupertypeString,
} from "../../../types/action";

import { EmitAction } from "../emit_action/emit_action";

import "./action_menu.css";
import type { TileId } from "../../../types/tile";
import {
  ActionDisambigMenu,
  type ActionDisambigMenuProps,
} from "../action_disambig_menu/action_disambig_menu";

function ActionMenuItem({
  action_supertype,
  actions,
  setDisambig,
}: {
  action_supertype: ActionSupertype;
  actions: ReadonlyArray<Action>;
  setDisambig: () => void;
}) {
  if (action_supertype == 0 || actions.length == 0) {
    return <></>;
  }
  const supertypeString = getActionSupertypeString(action_supertype);
  const emit_action = useContext(EmitAction);
  const onClick =
    actions.length == 1
      ? (e: Event) => {
          e.preventDefault();
          emit_action(actions[0]);
        }
      : (e: Event) => {
          e.preventDefault();
          setDisambig();
        };
  return (
    <button
      type="button"
      class={`action_button action_${action_supertype}`}
      data-text={supertypeString}
      onClick={onClick}
    >
      <div class="action_button_text">{supertypeString}</div>
    </button>
  );
}

export function ActionMenu({
  actions,
  last_discard,
}: {
  actions: ReadonlyArray<Action>;
  last_discard: TileId;
}) {
  const [actionDisambigMenuProps, setActionDisambigMenuProps] =
    useState<ActionDisambigMenuProps | null>(null);
  console.log(actions);
  const action_buckets: Action[][] = [[], [], [], [], [], [], [], []];
  for (const action of actions) {
    const action_supertype = getActionSupertype(action.action_type);
    action_buckets[action_supertype].push(action);
  }

  if (!actionDisambigMenuProps) {
    const actionMenuItems = action_buckets.map((actions, bucket_index) => (
      <ActionMenuItem
        action_supertype={bucket_index as ActionSupertype}
        actions={actions}
        setDisambig={() =>
          setActionDisambigMenuProps({
            action_supertype: bucket_index as ActionSupertype,
            actions: actions,
            last_discard: last_discard,
          })
        }
      />
    ));
    return <div id="actions">{actionMenuItems.reverse()}</div>;
  } else {
    return (
      <div id="actions_disambiguation">
        <ActionDisambigMenu
          props={actionDisambigMenuProps}
          unsetDisambig={() => setActionDisambigMenuProps(null)}
        />
      </div>
    );
  }
}
