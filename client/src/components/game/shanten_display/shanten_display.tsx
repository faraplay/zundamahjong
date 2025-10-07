import { useState } from "preact/hooks";

import type { TileId, TileValue } from "../../../types/tile";

import { Tile2DList } from "../tile_2d/tile_2d";

import "./shanten_display.css";

export function ShantenDisplay({
  shanten_info,
  visible,
}: {
  shanten_info: [number, Set<TileValue>];
  visible: boolean;
}) {
  const [shanten, tile_values] = shanten_info;
  const shanten_description = shanten == 0 ? "Tenpai" : `${shanten}-shanten`;
  return (
    <div class={`shanten_display ${visible ? "show" : "hide"}`}>
      <div class="shanten">{shanten_description}</div>
      <div class="tiles">
        <Tile2DList
          tiles={
            [...tile_values]
              .sort((a, b) => a - b)
              .map((tile_value) => tile_value * 10) as TileId[]
          }
        />
      </div>
    </div>
  );
}

export function ShantenDisplayButton({
  shanten_info,
}: {
  shanten_info: [number, Set<TileValue>];
}) {
  const [held, setHeld] = useState(false);
  const onMouseDown = (e: Event) => {
    e.preventDefault();
    setHeld(true);
  };
  const onMouseUp = (e: Event) => {
    e.preventDefault();
    setHeld(false);
  };
  return (
    <>
      <div
        class="shanten_display_button"
        onMouseDown={onMouseDown}
        onMouseUp={onMouseUp}
        onMouseLeave={onMouseUp}
      >
        ?
      </div>
      <ShantenDisplay shanten_info={shanten_info} visible={held} />
    </>
  );
}
