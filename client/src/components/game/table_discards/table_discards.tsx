import type { Discard } from "../../../types/game";

import { Tile3D } from "../tile_3d/tile_3d";

import "./table_discards.css";

export function TableDiscards({
  player_index,
  discards,
  riichi_discard_index,
}: {
  player_index: number;
  discards: ReadonlyArray<Discard>;
  riichi_discard_index: number | null;
}) {
  const riichiDiscards = discards.map((discard) => {
    return {
      ...discard,
      isFirstRiichi: false,
    };
  });
  if (riichi_discard_index !== null) {
    for (let i = riichi_discard_index; i < riichiDiscards.length; ++i) {
      const riichiDiscard = riichiDiscards[i];
      if (riichiDiscard.player == player_index && !riichiDiscard.is_called) {
        riichiDiscard.isFirstRiichi = true;
        break;
      }
    }
  }
  return (
    <div class={`player_discards player_${player_index}`}>
      {riichiDiscards
        .filter((riichiDiscard) => riichiDiscard.player == player_index)
        .map((riichiDiscard) => (
          <Tile3D key={riichiDiscard.tile} {...riichiDiscard} />
        ))}
    </div>
  );
}
