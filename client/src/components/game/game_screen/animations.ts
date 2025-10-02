import {
  ActionType,
  type Action,
  type AddKanAction,
  type ClosedKanAction,
  type HandTileAction,
  type OpenCallAction,
  type OpenKanAction,
  type SimpleAction,
} from "../../../types/action";
import type { HistoryItem } from "../../../types/game";

import "./animations.css";

function addAnimation(
  element: HTMLElement | null,
  animation_style: string,
  duration_milliseconds: number,
  delay_milliseconds: number,
) {
  if (!element) return duration_milliseconds;
  element.classList.add("animate");
  let animation = element.style.getPropertyValue("animation");
  let fill_mode = "both";
  if (animation) {
    animation += ",\n";
    fill_mode = "forwards";
  }
  animation += `${duration_milliseconds}ms ease-out ${delay_milliseconds}ms ${fill_mode} ${animation_style}`;
  element.style.setProperty("animation", animation);
}

function setDrawAnimation(
  player_index: number,
  _action: SimpleAction,
  delay_milliseconds: number,
) {
  const drawn_tile_element = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${player_index} .table_hand > *:last-child`,
  );
  addAnimation(drawn_tile_element, "drawAnimation", 250, delay_milliseconds);
  return 250;
}

function setDiscardAnimation(
  player_index: number,
  _action: HandTileAction,
  delay_milliseconds: number,
) {
  const discarded_tile_element = document.querySelector<HTMLElement>(
    `#discard_pool .player_discards.player_${player_index} > *:last-child`,
  );
  addAnimation(
    discarded_tile_element,
    "discardAnimation",
    250,
    delay_milliseconds,
  );
  return 250;
}

function setCallAnimation(
  player_index: number,
  _action: OpenCallAction,
  delay_milliseconds: number,
) {
  const call_element = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${player_index} > *:last-child`,
  );
  addAnimation(call_element, "callAnimation", 250, delay_milliseconds);
  return 250;
}

function setNewKanAnimation(
  player_index: number,
  _action: OpenKanAction | ClosedKanAction,
  delay_milliseconds: number,
) {
  const open_kan_element = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${player_index} > *:last-child`,
  );
  const drawn_tile_element = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${player_index} .table_hand > *:last-child`,
  );
  addAnimation(open_kan_element, "callAnimation", 250, delay_milliseconds);
  addAnimation(
    drawn_tile_element,
    "drawAnimation",
    250,
    delay_milliseconds + 250,
  );
  return 500;
}

function setAddKanAnimation(
  player_index: number,
  action: AddKanAction,
  delay_milliseconds: number,
) {
  const add_kan_tile = document.querySelector<HTMLElement>(
    `.tile_id_${action.tile}`,
  );
  const drawn_tile_element = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${player_index} .table_hand > *:last-child`,
  );
  addAnimation(add_kan_tile, "addKanAnimation", 250, delay_milliseconds);
  addAnimation(
    drawn_tile_element,
    "drawAnimation",
    250,
    delay_milliseconds + 250,
  );
  return 500;
}

function setFlowerAnimation(
  player_index: number,
  action: HandTileAction,
  delay_milliseconds: number,
) {
  const flower_element = document.querySelector<HTMLElement>(
    `.tile_id_${action.tile}`,
  );
  const flower_drawn_tile_element = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${player_index} .table_hand > *:last-child`,
  );
  addAnimation(flower_element, "callAnimation", 250, delay_milliseconds);
  addAnimation(
    flower_drawn_tile_element,
    "drawAnimation",
    250,
    delay_milliseconds + 250,
  );
  return 500;
}

function setWinAnimation(
  player_index: number,
  _action: SimpleAction,
  delay_milliseconds: number,
) {
  const win_info = document.querySelector<HTMLElement>("#win_info");
  const win_hand_element = document.querySelector<HTMLElement>(
    `.table_hand_outer.player_${player_index} .table_hand`,
  );
  addAnimation(win_hand_element, "winAnimation", 500, delay_milliseconds);
  addAnimation(win_info, "showAnimation", 0, delay_milliseconds + 1000);
  return 1000;
}

function setAnimation(
  player_index: number,
  action: Action,
  delay_milliseconds: number,
) {
  switch (action.action_type) {
    case ActionType.DRAW:
      return setDrawAnimation(player_index, action, delay_milliseconds);
    case ActionType.DISCARD:
      return setDiscardAnimation(player_index, action, delay_milliseconds);
    case ActionType.CHII:
    case ActionType.PON:
      return setCallAnimation(player_index, action, delay_milliseconds);
    case ActionType.OPEN_KAN:
    case ActionType.CLOSED_KAN:
      return setNewKanAnimation(player_index, action, delay_milliseconds);
    case ActionType.ADD_KAN:
      return setAddKanAnimation(player_index, action, delay_milliseconds);
    case ActionType.FLOWER:
      return setFlowerAnimation(player_index, action, delay_milliseconds);
    case ActionType.RON:
    case ActionType.TSUMO:
      return setWinAnimation(player_index, action, delay_milliseconds);
    default:
      return 0;
  }
}

function unsetAnimations() {
  const animated_elements = document.querySelectorAll<HTMLElement>(".animate");
  for (const animated_element of animated_elements) {
    animated_element.classList.remove("animate");
    animated_element.style.setProperty("animation", "");
  }
}

export function setAnimations(history_updates: ReadonlyArray<HistoryItem>) {
  unsetAnimations();
  let delay_milliseconds = 0;
  for (const history_item of history_updates) {
    delay_milliseconds += setAnimation(
      history_item.player_index,
      history_item.action,
      delay_milliseconds,
    );
  }
}
