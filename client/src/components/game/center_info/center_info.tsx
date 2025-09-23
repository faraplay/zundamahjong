import type { GameInfo } from "../../../types/game";

import "./center_info.css";

const player_winds = ["東", "南", "西", "北"];

function CenterInfoPlayer({
  player_index,
  seat_wind,
  score,
  is_current_player,
}: {
  player_index: number;
  seat_wind: string;
  score: number | null;
  is_current_player: boolean;
}) {
  return (
    <>
      <span class={`player_indicator player_${player_index}`}>{seat_wind}</span>
      <span class={`score player_${player_index}`}>
        {score == null ? "" : score}
      </span>
      <span
        class={
          `turn_indicator player_${player_index}` +
          (is_current_player ? " current_player" : "")
        }
      ></span>
    </>
  );
}

export function CenterInfo({
  game_info,
  tiles_left,
  current_player,
}: {
  game_info: GameInfo;
  tiles_left: number;
  current_player: number;
}) {
  const centerInfoPlayers = [];
  const player_count = game_info.player_scores.length;
  for (let index = 0; index < player_count; ++index) {
    centerInfoPlayers.push({
      player_index: index,
      seat_wind:
        player_winds[
          (index - game_info.sub_round + player_count) % player_count
        ],
      score: game_info.player_scores[index],
      is_current_player: index == current_player,
    });
  }
  for (let index = player_count; index < 4; ++index) {
    centerInfoPlayers.push({
      player_index: index,
      seat_wind: "",
      score: null,
      is_current_player: false,
    });
  }
  return (
    <div id="table_center_info">
      <p id="wind_sub_round">
        {player_winds[game_info.wind_round] +
          String(game_info.sub_round + 1) +
          "-" +
          String(game_info.draw_count)}
      </p>
      <p id="tiles_left">{tiles_left}</p>
      <div id="scores">
        {centerInfoPlayers.map((info) => CenterInfoPlayer(info))}
      </div>
    </div>
  );
}
