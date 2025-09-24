import {
  type Action,
  type ActionSupertype,
  getActionSupertype,
  getActionSupertypeString,
} from "../../../types/action";

import "./action_menu.css";

function ActionMenuItem({
  action_supertype,
  actions,
}: {
  action_supertype: ActionSupertype;
  actions: ReadonlyArray<Action>;
}) {
  if (action_supertype == 0) {
    return <></>;
  }
  const supertypeString = getActionSupertypeString(action_supertype);
  return (
    <button
      type="button"
      class={`action_button action_${action_supertype}`}
      data-text={supertypeString}
    >
      <div class="action_button_text">{supertypeString}</div>
    </button>
  );
}

export function ActionMenu({ actions }: { actions: ReadonlyArray<Action> }) {
  const action_buckets: Action[][] = [[], [], [], [], [], [], [], []];
  for (const action of actions) {
    const action_supertype = getActionSupertype(action.action_type);
    action_buckets[action_supertype].push(action);
  }
  return (
    <div id="actions">
      {action_buckets
        .map((actions, bucket_index) => (
          <ActionMenuItem
            action_supertype={bucket_index as ActionSupertype}
            actions={actions}
          />
        ))
        .reverse()}
    </div>
  );
}
