import type { Call, Win } from "../../../types/game";

import { Tile2D } from "../tile_2d/tile_2d";

import "./win_hand.css";

function WinCall({ call }: { call: Call }) {
  return (
    <span class="call">
      {call.tiles.map((tile) => (
        <Tile2D tile={tile} />
      ))}
    </span>
  );
}

export function WinHand({ win_info }: { win_info: Win | null }) {
  if (!win_info) {
    return <></>;
  }
  const win_hand_width = win_info.calls.reduce(
    (partial_sum, call) => partial_sum + call.tiles.length + 0.5,
    win_info.hand.length,
  );
  const flowerOverlap = win_hand_width + win_info.flowers.length >= 21.5;
  return (
    <div id="win_hand">
      <div id="win_flowers" class={flowerOverlap ? "overlap" : ""}>
        {win_info.flowers.map((tile) => (
          <Tile2D tile={tile} />
        ))}
      </div>
      <div id="win_tiles">
        {win_info.hand.map((tile) => (
          <Tile2D tile={tile} />
        ))}
      </div>
      <div id="win_calls">
        {win_info.calls.map((call) => (
          <WinCall call={call} />
        ))}
      </div>
    </div>
  );
}
