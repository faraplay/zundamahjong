import type { AllServerInfo } from "../../../types/game";
import type { TileId } from "../../../types/tile";

import { CenterInfo } from "../center_info/center_info";
import { TableCalls } from "../table_calls/table_calls";
import { TableDiscards } from "../table_discards/table_discards";
import { TableFlowers } from "../table_flowers/table_flowers";
import { TableHand } from "../table_hand/table_hand";

import "./table.css";

export function Table({ info }: { info: AllServerInfo }) {
  const known_hands: ReadonlyArray<TileId>[] = [];
  for (const hand_count of info.round_info.hand_counts) {
    known_hands.push(Array<TileId>(hand_count).fill(0));
  }
  known_hands[info.player_index] = info.player_info.hand;
  if (info.win_info) {
    known_hands[info.win_info.win_player] = info.win_info.hand;
  }

  const player_discards: TileId[][] = [];
  for (let player_index = 0; player_index < info.player_count; ++player_index) {
    player_discards.push(
      info.round_info.discards
        .filter((discard) => discard.player == player_index)
        .map((discard) => discard.tile),
    );
  }
  return (
    <div id="table">
      <CenterInfo
        game_info={info.game_info}
        tiles_left={info.round_info.tiles_left}
        current_player={info.round_info.current_player}
      />
      <div id="table_hands">
        {known_hands.map((hand, index) => (
          <TableHand key={index} player_index={index} tiles={hand} />
        ))}
      </div>
      <div id="calls_list">
        {info.round_info.calls.map((player_calls, index) => (
          <TableCalls key={index} player_index={index} calls={player_calls} />
        ))}
      </div>
      <div id="flowers_list">
        {info.round_info.flowers.map((tiles, index) => (
          <TableFlowers key={index} player_index={index} tiles={tiles} />
        ))}
      </div>
      <div id="discard_pool">
        {player_discards.map((tiles, index) => (
          <TableDiscards key={index} player_index={index} tiles={tiles} />
        ))}
      </div>
    </div>
  );
}
