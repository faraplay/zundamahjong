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
  animationStyle: string,
  durationMilliseconds: number,
  delayMilliseconds: number,
) {
  if (!element) return durationMilliseconds;
  element.classList.add("animate");
  let animation = element.style.getPropertyValue("animation");
  let fillMode = "both";
  if (animation) {
    animation += ",\n";
    fillMode = "forwards";
  }
  animation += `${durationMilliseconds}ms ease-out ${delayMilliseconds}ms ${fillMode} ${animationStyle}`;
  element.style.setProperty("animation", animation);
}

function setDrawAnimation(
  playerIndex: number,
  _avatarId: number,
  _action: Action,
  delayMilliseconds: number,
) {
  const drawnTileElement = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${playerIndex} .table_hand > *:last-child`,
  );
  addAnimation(drawnTileElement, "drawAnimation", 250, delayMilliseconds);
  return 250;
}

function setDiscardAnimation(
  playerIndex: number,
  _avatarId: number,
  _action: Action,
  delayMilliseconds: number,
) {
  const discardedTileElement = document.querySelector<HTMLElement>(
    `#discard_pool .player_discards.player_${playerIndex} > *:last-child`,
  );
  const discardAudioElement =
    document.querySelector<HTMLAudioElement>("audio.discard");
  addAnimation(
    discardedTileElement,
    "discardAnimation",
    250,
    delayMilliseconds,
  );
  setTimeout(() => {
    discardAudioElement?.play();
  }, delayMilliseconds + 125);
  return 250;
}

function setCallAnimation(
  playerIndex: number,
  avatarId: number,
  _action: Action,
  delayMilliseconds: number,
  callType: "chii" | "pon",
) {
  const callElement = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${playerIndex} > *:last-child`,
  );
  const callAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.${callType}`,
  );
  setTimeout(() => {
    callAudioElement?.play();
  }, delayMilliseconds);
  addAnimation(callElement, "callAnimation", 250, delayMilliseconds);
  return 250;
}

function setChiiAnimation(
  playerIndex: number,
  avatarId: number,
  _action: Action,
  delayMilliseconds: number,
) {
  return setCallAnimation(
    playerIndex,
    avatarId,
    _action,
    delayMilliseconds,
    "chii",
  );
}

function setPonAnimation(
  playerIndex: number,
  avatarId: number,
  _action: Action,
  delayMilliseconds: number,
) {
  return setCallAnimation(
    playerIndex,
    avatarId,
    _action,
    delayMilliseconds,
    "pon",
  );
}

function setNewKanAnimation(
  playerIndex: number,
  avatarId: number,
  _action: Action,
  delayMilliseconds: number,
) {
  const openKanElement = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${playerIndex} > *:last-child`,
  );
  const drawnTileElement = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${playerIndex} .table_hand > *:last-child`,
  );
  const kanAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.kan`,
  );
  setTimeout(() => {
    kanAudioElement?.play();
  }, delayMilliseconds);
  addAnimation(openKanElement, "callAnimation", 250, delayMilliseconds);
  addAnimation(drawnTileElement, "drawAnimation", 250, delayMilliseconds + 250);
  return 500;
}

function setAddKanAnimation(
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
) {
  const addKanTile = document.querySelector<HTMLElement>(
    `.tile_id_${(action as AddKanAction).tile}`,
  );
  const drawnTileElement = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${playerIndex} .table_hand > *:last-child`,
  );
  const kanAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.kan`,
  );
  setTimeout(() => {
    kanAudioElement?.play();
  }, delayMilliseconds);
  addAnimation(addKanTile, "addKanAnimation", 250, delayMilliseconds);
  addAnimation(drawnTileElement, "drawAnimation", 250, delayMilliseconds + 250);
  return 500;
}

function setFlowerAnimation(
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
) {
  const flowerElement = document.querySelector<HTMLElement>(
    `.tile_id_${(action as HandTileAction).tile}`,
  );
  const flower_drawnTileElement = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${playerIndex} .table_hand > *:last-child`,
  );
  const faAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.fa`,
  );
  setTimeout(() => {
    faAudioElement?.play();
  }, delayMilliseconds);
  addAnimation(flowerElement, "callAnimation", 250, delayMilliseconds);
  addAnimation(
    flower_drawnTileElement,
    "drawAnimation",
    250,
    delayMilliseconds + 250,
  );
  return 500;
}

function setWinAnimation(
  playerIndex: number,
  avatarId: number,
  _action: Action,
  delayMilliseconds: number,
  winType: "ron" | "tsumo",
) {
  const winInfo = document.querySelector<HTMLElement>("#win_info");
  const winHandElement = document.querySelector<HTMLElement>(
    `.table_hand_outer.player_${playerIndex} .table_hand`,
  );
  const winAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.${winType}`,
  );
  setTimeout(() => {
    winAudioElement?.play();
  }, delayMilliseconds);
  addAnimation(winHandElement, "winAnimation", 500, delayMilliseconds);
  addAnimation(winInfo, "showAnimation", 0, delayMilliseconds + 1000);
  return 1000;
}

function setRonAnimation(
  playerIndex: number,
  avatarId: number,
  _action: Action,
  delayMilliseconds: number,
) {
  return setWinAnimation(
    playerIndex,
    avatarId,
    _action,
    delayMilliseconds,
    "ron",
  );
}

function setTsumoAnimation(
  playerIndex: number,
  avatarId: number,
  _action: Action,
  delayMilliseconds: number,
) {
  return setWinAnimation(
    playerIndex,
    avatarId,
    _action,
    delayMilliseconds,
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
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
) {
  const setAnimationFunc = setAnimationFuncs[action.action_type];
  return setAnimationFunc(playerIndex, avatarId, action, delayMilliseconds);
}

function unsetAnimations() {
  const animatedElements = document.querySelectorAll<HTMLElement>(".animate");
  for (const animatedElement of animatedElements) {
    animatedElement.classList.remove("animate");
    animatedElement.style.setProperty("animation", "");
  }
}

export function setAnimations(
  historyUpdates: ReadonlyArray<HistoryItem>,
  avatarIds: number[],
) {
  unsetAnimations();
  let delayMilliseconds = 0;
  for (const historyItem of historyUpdates) {
    delayMilliseconds += setAnimation(
      historyItem.player_index,
      avatarIds[historyItem.player_index],
      historyItem.action,
      delayMilliseconds,
    );
  }
}
