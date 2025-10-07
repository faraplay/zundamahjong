import { calculate_shanten } from "./shanten";
import type { AllInfo, AllServerInfo } from "./types/game";
import type { TileValue } from "./types/tile";

export function processInfo(info: AllServerInfo): AllInfo {
  const allInfo: AllInfo = info;
  const tile_values = info.player_info.hand.map(
    (tile) => Math.trunc(tile / 10) as TileValue,
  );
  if (info.player_info.hand.length % 3 == 1) {
    const shanten_info = calculate_shanten(tile_values);
    allInfo.player_info.shanten_info = shanten_info;
  } else if (info.player_info.hand.length % 3 == 2) {
    const discard_shanten_info = Object.fromEntries(
      info.player_info.hand.map((tile, index) => {
        const discarded_tile_values = [...tile_values];
        discarded_tile_values.splice(index, 1);
        return [tile, calculate_shanten(discarded_tile_values)];
      }),
    );
    allInfo.player_info.discard_shanten_info = discard_shanten_info;
  }
  return allInfo;
}
