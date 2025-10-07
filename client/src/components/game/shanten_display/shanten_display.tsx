import { useState } from "preact/hooks";

import type { TileId, TileValue } from "../../../types/tile";

import { Tile2D } from "../tile_2d/tile_2d";

import "./shanten_display.css";

export function ShantenDisplay({
  shantenInfo,
  remainingTileCounts,
  visible,
}: {
  shantenInfo: [number, Set<TileValue>];
  remainingTileCounts: number[];
  visible: boolean;
}) {
  const [shanten, tileValuesSet] = shantenInfo;
  const tileValues = [...tileValuesSet].sort((a, b) => a - b);
  const improveTileCount = tileValues.reduce<number>(
    (sum, tileValue) => sum + remainingTileCounts[tileValue],
    0,
  );
  const shantenDescription =
    shanten == 0 ? "Tenpai" : `${shanten}-shanten (${improveTileCount} tiles)`;
  return (
    <div class={`shanten_display ${visible ? "show" : "hide"}`}>
      <div class="shanten">{shantenDescription}</div>
      <div class="tiles">
        {tileValues.map((tile) => (
          <div key={tile} class="shanten_item">
            <Tile2D tile={(tile * 10) as TileId} />
            <div class="tile_freq">{`${remainingTileCounts[tile]} left`}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function ShantenDisplayButton({
  shantenInfo,
  remainingTileCounts,
}: {
  shantenInfo: [number, Set<TileValue>];
  remainingTileCounts: number[];
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
      <ShantenDisplay
        shantenInfo={shantenInfo}
        remainingTileCounts={remainingTileCounts}
        visible={held}
      />
    </>
  );
}
