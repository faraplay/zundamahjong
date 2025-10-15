import {
  ActionType,
  type Action,
  type AddKanAction,
  type HandTileAction,
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
  _avatarId: number,
  _action: Action,
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
  _avatarId: number,
  _action: Action,
  delay_milliseconds: number,
) {
  const discarded_tile_element = document.querySelector<HTMLElement>(
    `#discard_pool .player_discards.player_${player_index} > *:last-child`,
  );
  const discardAudioElement =
    document.querySelector<HTMLAudioElement>("audio.discard");
  addAnimation(
    discarded_tile_element,
    "discardAnimation",
    250,
    delay_milliseconds,
  );
  setTimeout(() => {
    discardAudioElement?.play();
  }, delay_milliseconds + 125);
  return 250;
}

function setCallAnimation(
  player_index: number,
  avatarId: number,
  _action: Action,
  delay_milliseconds: number,
  callType: "chii" | "pon",
) {
  const call_element = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${player_index} > *:last-child`,
  );
  const callAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.${callType}`,
  );
  setTimeout(() => {
    callAudioElement?.play();
  }, delay_milliseconds);
  addAnimation(call_element, "callAnimation", 250, delay_milliseconds);
  return 250;
}

function setChiiAnimation(
  player_index: number,
  avatarId: number,
  _action: Action,
  delay_milliseconds: number,
) {
  return setCallAnimation(
    player_index,
    avatarId,
    _action,
    delay_milliseconds,
    "chii",
  );
}

function setPonAnimation(
  player_index: number,
  avatarId: number,
  _action: Action,
  delay_milliseconds: number,
) {
  return setCallAnimation(
    player_index,
    avatarId,
    _action,
    delay_milliseconds,
    "pon",
  );
}

function setNewKanAnimation(
  player_index: number,
  avatarId: number,
  _action: Action,
  delay_milliseconds: number,
) {
  const open_kan_element = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${player_index} > *:last-child`,
  );
  const drawn_tile_element = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${player_index} .table_hand > *:last-child`,
  );
  const kanAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.kan`,
  );
  setTimeout(() => {
    kanAudioElement?.play();
  }, delay_milliseconds);
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
  avatarId: number,
  action: Action,
  delay_milliseconds: number,
) {
  const add_kan_tile = document.querySelector<HTMLElement>(
    `.tile_id_${(action as AddKanAction).tile}`,
  );
  const drawn_tile_element = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${player_index} .table_hand > *:last-child`,
  );
  const kanAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.kan`,
  );
  setTimeout(() => {
    kanAudioElement?.play();
  }, delay_milliseconds);
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
  avatarId: number,
  action: Action,
  delay_milliseconds: number,
) {
  const flower_element = document.querySelector<HTMLElement>(
    `.tile_id_${(action as HandTileAction).tile}`,
  );
  const flower_drawn_tile_element = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${player_index} .table_hand > *:last-child`,
  );
  const faAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.fa`,
  );
  setTimeout(() => {
    faAudioElement?.play();
  }, delay_milliseconds);
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
  avatarId: number,
  _action: Action,
  delay_milliseconds: number,
  winType: "ron" | "tsumo",
) {
  const win_info = document.querySelector<HTMLElement>("#win_info");
  const win_hand_element = document.querySelector<HTMLElement>(
    `.table_hand_outer.player_${player_index} .table_hand`,
  );
  const winAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.${winType}`,
  );
  setTimeout(() => {
    winAudioElement?.play();
  }, delay_milliseconds);
  addAnimation(win_hand_element, "winAnimation", 500, delay_milliseconds);
  addAnimation(win_info, "showAnimation", 0, delay_milliseconds + 1000);
  return 1000;
}

function setRonAnimation(
  player_index: number,
  avatarId: number,
  _action: Action,
  delay_milliseconds: number,
) {
  return setWinAnimation(
    player_index,
    avatarId,
    _action,
    delay_milliseconds,
    "ron",
  );
}

function setTsumoAnimation(
  player_index: number,
  avatarId: number,
  _action: Action,
  delay_milliseconds: number,
) {
  return setWinAnimation(
    player_index,
    avatarId,
    _action,
    delay_milliseconds,
    "tsumo",
  );
}

const setAnimationFuncs = {
  [ActionType.PASS]: () => {
    return 0;
  },
  [ActionType.CONTINUE]: () => {
    return 0;
  },
  [ActionType.DRAW]: setDrawAnimation,
  [ActionType.DISCARD]: setDiscardAnimation,
  [ActionType.CHII]: setChiiAnimation,
  [ActionType.PON]: setPonAnimation,
  [ActionType.OPEN_KAN]: setNewKanAnimation,
  [ActionType.CLOSED_KAN]: setNewKanAnimation,
  [ActionType.ADD_KAN]: setAddKanAnimation,
  [ActionType.FLOWER]: setFlowerAnimation,
  [ActionType.RON]: setRonAnimation,
  [ActionType.TSUMO]: setTsumoAnimation,
} as const;

function setAnimation(
  player_index: number,
  avatarId: number,
  action: Action,
  delay_milliseconds: number,
) {
  const setAnimationFunc = setAnimationFuncs[action.action_type];
  return setAnimationFunc(player_index, avatarId, action, delay_milliseconds);
}

function unsetAnimations() {
  const animated_elements = document.querySelectorAll<HTMLElement>(".animate");
  for (const animated_element of animated_elements) {
    animated_element.classList.remove("animate");
    animated_element.style.setProperty("animation", "");
  }
}

export function setAnimations(
  history_updates: ReadonlyArray<HistoryItem>,
  avatars: number[],
) {
  unsetAnimations();
  let delay_milliseconds = 0;
  for (const history_item of history_updates) {
    delay_milliseconds += setAnimation(
      history_item.player_index,
      avatars[history_item.player_index],
      history_item.action,
      delay_milliseconds,
    );
  }
}
