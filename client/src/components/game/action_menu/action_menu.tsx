import { useContext, useState } from "preact/hooks";
import {
  type Action,
  type ActionSupertype,
  getActionSupertype,
  getActionSupertypeString,
} from "../../../types/action";

import { EmitAction } from "../emit_action/emit_action";

import "./action_menu.css";
import { ActionDisambigMenu } from "../action_disambig_menu/action_disambig_menu";

function ActionMenuItem({
  action_supertype,
  actions,
  setDisambig,
}: {
  action_supertype: ActionSupertype;
  actions: ReadonlyArray<Action>;
  setDisambig: () => void;
}) {
  const emit_action = useContext(EmitAction);
  if (action_supertype == 0 || actions.length == 0) {
    return <></>;
  }
  const supertypeString = getActionSupertypeString(action_supertype);
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

export function ActionMenu({ actions }: { actions: ReadonlyArray<Action> }) {
  const [disambigActions, setDisambigActions] =
    useState<ReadonlyArray<Action> | null>(null);
  if (actions.length <= 1) {
    return <></>;
  }
  const action_buckets: Action[][] = [[], [], [], [], [], [], [], []];
  for (const action of actions) {
    const action_supertype = getActionSupertype(action.action_type);
    action_buckets[action_supertype].push(action);
  }

  if (!disambigActions) {
    const actionMenuItems = action_buckets.map((actions, bucket_index) => (
      <ActionMenuItem
        key={bucket_index}
        action_supertype={bucket_index as ActionSupertype}
        actions={actions}
        setDisambig={() => setDisambigActions(actions)}
      />
    ));
    return <div id="actions">{actionMenuItems.reverse()}</div>;
  }
  return (
    <div id="actions_disambiguation">
      <ActionDisambigMenu
        disambigActions={disambigActions}
        unsetDisambig={() => setDisambigActions(null)}
      />
    </div>
  );
}
