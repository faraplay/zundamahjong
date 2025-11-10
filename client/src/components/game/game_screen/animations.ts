import {
  ActionType,
  getActionSupertype,
  type Action,
  type AddKanAction,
  type HandTileAction,
} from "../../../types/action";
import type { HistoryItem } from "../../../types/game";

import "./animations.css";

function addAudio(
  audioElement: HTMLAudioElement | null,
  delayMilliseconds: number,
) {
  if (!audioElement) {
    return;
  }
  setTimeout(() => {
    audioElement.play();
  }, delayMilliseconds);
}

function addAnimation(
  element: HTMLElement | null,
  animationStyle: string,
  durationMilliseconds: number,
  delayMilliseconds: number,
) {
  if (!element) return durationMilliseconds;
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
  action: Action,
  delayMilliseconds: number,
) {
  if (action.action_type != ActionType.DISCARD) {
    return 0;
  }
  const discardedTileElement = document.querySelector<HTMLElement>(
    `#discard_pool .player_discards.player_${playerIndex} .tile_3d.tile_id_${action.tile}`,
  );
  const discardAudioElement =
    document.querySelector<HTMLAudioElement>("audio.discard");
  addAnimation(
    discardedTileElement,
    "discardAnimation",
    250,
    delayMilliseconds,
  );
  addAudio(discardAudioElement, delayMilliseconds + 125);
  return 250;
}

function setRiichiAnimation(
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
) {
  if (action.action_type != ActionType.RIICHI) {
    return 0;
  }
  const cutinElement = document.querySelector<HTMLElement>(
    `.cutins .cutin.action_${getActionSupertype(action.action_type)}.player_${playerIndex}`,
  );
  const discardedTileElement = document.querySelector<HTMLElement>(
    `#discard_pool .player_discards.player_${playerIndex} .tile_3d.tile_id_${action.tile}`,
  );
  const riichiAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.riichi`,
  );
  const discardAudioElement =
    document.querySelector<HTMLAudioElement>("audio.discard");
  addAudio(riichiAudioElement, delayMilliseconds);
  addAnimation(cutinElement, "cutinAnimation", 1000, delayMilliseconds);
  addAnimation(
    discardedTileElement,
    "discardAnimation",
    250,
    delayMilliseconds + 1000,
  );
  addAudio(discardAudioElement, delayMilliseconds + 1125);
  return 1250;
}

function setCallAnimation(
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
  callType: "chii" | "pon",
) {
  const cutinElement = document.querySelector<HTMLElement>(
    `.cutins .cutin.action_${getActionSupertype(action.action_type)}.player_${playerIndex}`,
  );
  const callElement = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${playerIndex} > *:last-child`,
  );
  const callAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.${callType}`,
  );
  addAudio(callAudioElement, delayMilliseconds);
  addAnimation(cutinElement, "cutinAnimation", 1000, delayMilliseconds);
  addAnimation(callElement, "callAnimation", 250, delayMilliseconds + 1000);
  return 1250;
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
  action: Action,
  delayMilliseconds: number,
) {
  const cutinElement = document.querySelector<HTMLElement>(
    `.cutins .cutin.action_${getActionSupertype(action.action_type)}.player_${playerIndex}`,
  );
  const openKanElement = document.querySelector<HTMLElement>(
    `#calls_list .player_calls.player_${playerIndex} > *:last-child`,
  );
  const drawnTileElement = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${playerIndex} .table_hand > *:last-child`,
  );
  const kanAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.kan`,
  );
  addAudio(kanAudioElement, delayMilliseconds);
  addAnimation(cutinElement, "cutinAnimation", 1000, delayMilliseconds);
  addAnimation(openKanElement, "callAnimation", 250, delayMilliseconds + 1000);
  addAnimation(
    drawnTileElement,
    "drawAnimation",
    250,
    delayMilliseconds + 1250,
  );
  return 1500;
}

function setAddKanAnimation(
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
) {
  const cutinElement = document.querySelector<HTMLElement>(
    `.cutins .cutin.action_${getActionSupertype(action.action_type)}.player_${playerIndex}`,
  );
  const addKanTile = document.querySelector<HTMLElement>(
    `.tile_id_${(action as AddKanAction).tile}`,
  );
  const drawnTileElement = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${playerIndex} .table_hand > *:last-child`,
  );
  const kanAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.kan`,
  );
  addAudio(kanAudioElement, delayMilliseconds);
  addAnimation(cutinElement, "cutinAnimation", 1000, delayMilliseconds);
  addAnimation(addKanTile, "addKanAnimation", 250, delayMilliseconds + 1000);
  addAnimation(
    drawnTileElement,
    "drawAnimation",
    250,
    delayMilliseconds + 1250,
  );
  return 1500;
}

function setFlowerAnimation(
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
) {
  const cutinElement = document.querySelector<HTMLElement>(
    `.cutins .cutin.action_${getActionSupertype(action.action_type)}.player_${playerIndex}`,
  );
  const flowerElement = document.querySelector<HTMLElement>(
    `.tile_id_${(action as HandTileAction).tile}`,
  );
  const flower_drawnTileElement = document.querySelector<HTMLElement>(
    `#table_hands .table_hand_outer.player_${playerIndex} .table_hand > *:last-child`,
  );
  const faAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.fa`,
  );
  addAudio(faAudioElement, delayMilliseconds);
  addAnimation(cutinElement, "cutinAnimation", 500, delayMilliseconds);
  addAnimation(flowerElement, "callAnimation", 250, delayMilliseconds + 500);
  addAnimation(
    flower_drawnTileElement,
    "drawAnimation",
    250,
    delayMilliseconds + 750,
  );
  return 1000;
}

function setWinAnimation(
  playerIndex: number,
  avatarId: number,
  action: Action,
  delayMilliseconds: number,
  winType: "ron" | "tsumo",
) {
  const cutinElement = document.querySelector<HTMLElement>(
    `.cutins .cutin.action_${getActionSupertype(action.action_type)}.player_${playerIndex}`,
  );
  const winHandElement = document.querySelector<HTMLElement>(
    `.table_hand_outer.player_${playerIndex} .table_hand`,
  );
  const winAudioElement = document.querySelector<HTMLAudioElement>(
    `audio.avatar_${avatarId}.${winType}`,
  );
  addAudio(winAudioElement, delayMilliseconds);
  addAnimation(cutinElement, "cutinAnimation", 1000, delayMilliseconds);
  addAnimation(winHandElement, "winAnimation", 500, delayMilliseconds + 1000);
  return 2000;
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

function setFinalAnimation(delayMilliseconds: number) {
  let extraDelay = 0;
  const drawnHandTile = document.querySelector<HTMLElement>(
    "#hand .hand_tile_button.drawn_tile",
  );
  if (drawnHandTile) {
    addAnimation(drawnHandTile, "fadeInAnimation", 50, delayMilliseconds);
    extraDelay += 50;
  }
  const actionsMenu = document.querySelector<HTMLElement>("#actions");
  if (actionsMenu) {
    addAnimation(
      actionsMenu,
      "showAnimation",
      0,
      delayMilliseconds + extraDelay,
    );
  }
  const winInfo = document.querySelector<HTMLElement>("#win_info");
  if (winInfo) {
    addAnimation(winInfo, "showAnimation", 0, delayMilliseconds + extraDelay);
  }
  return extraDelay;
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
  [ActionType.RIICHI]: setRiichiAnimation,
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
  const animatedElements = document.querySelectorAll<HTMLElement>(
    `*[style*="animation:"]`,
  );
  for (const animatedElement of animatedElements) {
    animatedElement.style.setProperty("animation", "");
  }
}

export function setAnimations(
  historyUpdates: ReadonlyArray<HistoryItem>,
  avatarIds: number[],
) {
  console.log(historyUpdates);
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
  setFinalAnimation(delayMilliseconds);
}
