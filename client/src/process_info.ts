import { calculate_shanten } from "./shanten";
import { getCallTiles } from "./types/call";
import type { AllServerInfo } from "./types/game";
import { tileValueTop, type TileId, type TileValue } from "./types/tile";

export type AllInfo = AllServerInfo & {
  player_info: {
    shanten_info?: [number, Set<TileValue>];
    discard_shanten_info?: {
      [tile in TileId]?: [number, Set<TileValue>];
    };
    remaining_tile_counts: number[];
  };
};

export function processInfo(info: AllServerInfo): AllInfo {
  let shantenInfo: [number, Set<TileValue>] | undefined;
  let discardShantenInfo:
    | {
        [tile in TileId]?: [number, Set<TileValue>];
      }
    | undefined;

  const tileValues = info.player_info.hand.map(
    (tile) => Math.trunc(tile / 10) as TileValue,
  );
  if (info.player_info.hand.length % 3 == 1) {
    shantenInfo = calculate_shanten(tileValues, info.player_count == 3);
  } else if (info.player_info.hand.length % 3 == 2) {
    discardShantenInfo = Object.fromEntries(
      info.player_info.hand.map((tile, index) => {
        const discarded_tile_values = [...tileValues];
        discarded_tile_values.splice(index, 1);
        return [
          tile,
          calculate_shanten(discarded_tile_values, info.player_count == 3),
        ];
      }),
    );
  }

  const visibleTiles = [
    ...info.round_info.discards.map((discard) => discard.tile),
    ...info.round_info.calls.flat(1).flatMap((call) => getCallTiles(call)),
    ...info.player_info.hand,
  ];
  const deckTileValues =
    info.player_count == 4
      ? [
          1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22,
          23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37,
        ]
      : [
          1, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27,
          28, 29, 31, 32, 33, 34, 35, 36, 37,
        ];
  const remainingTileCounts = Array(tileValueTop).fill(0);
  for (const tileValue of deckTileValues) {
    remainingTileCounts[tileValue] = 4;
  }
  for (const tile of visibleTiles) {
    remainingTileCounts[Math.trunc(tile / 10)] -= 1;
  }

  return {
    ...info,
    player_info: {
      ...info.player_info,
      shanten_info: shantenInfo,
      discard_shanten_info: discardShantenInfo,
      remaining_tile_counts: remainingTileCounts,
    },
  };
}
