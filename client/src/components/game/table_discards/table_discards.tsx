import type { Discard } from "../../../types/game";

import { Tile3D } from "../tile_3d/tile_3d";

import "./table_discards.css";

export function TableDiscards({
  player_index,
  discards,
}: {
  player_index: number;
  discards: ReadonlyArray<Discard>;
}) {
  const firstRiichiIndex = discards.findIndex((discard) => discard.is_riichi);
  return (
    <div class={`player_discards player_${player_index}`}>
      {discards.map((discard, index) => (
        <Tile3D
          key={discard.tile}
          tile={discard.tile}
          isFirstRiichi={index == firstRiichiIndex}
        />
      ))}
    </div>
  );
}
