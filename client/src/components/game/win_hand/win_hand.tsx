import { CallType, getCallTiles, type Call } from "../../../types/call";
import type { Win } from "../../../types/game";

import { Tile2D, Tile2DBack, Tile2DList } from "../tile_2d/tile_2d";

import "./win_hand.css";

function WinCall({ call }: { call: Call }) {
  if (call.call_type == CallType.CLOSED_KAN) {
    return (
      <span class="call">
        <Tile2DBack />
        <Tile2D tile={call.tiles[1]} />
        <Tile2D tile={call.tiles[2]} />
        <Tile2DBack />
      </span>
    );
  }
  return (
    <span class="call">
      <Tile2DList tiles={getCallTiles(call)} />
    </span>
  );
}

export function WinHand({ win_info }: { win_info: Win | null }) {
  if (!win_info) {
    return <></>;
  }
  const win_hand_width = win_info.calls.reduce(
    (partial_sum, call) => partial_sum + getCallTiles(call).length + 0.5,
    win_info.hand.length + 0.5,
  );
  const flowerOverlap = win_hand_width + win_info.flowers.length >= 21.5;
  return (
    <div class="win_hand">
      <div class={`win_flowers ${flowerOverlap ? "overlap" : ""}`}>
        <Tile2DList tiles={win_info.flowers} />
      </div>
      <div class="win_tiles">
        <Tile2DList tiles={win_info.hand} />
      </div>
      <div class="win_calls">
        {win_info.calls.map((call) => (
          <WinCall key={call} call={call} />
        ))}
      </div>
    </div>
  );
}
