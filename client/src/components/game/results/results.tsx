import { useContext } from "preact/hooks";
import type { AllInfo } from "../../../types/game";

import "./results.css";
import { Emitter } from "../../emitter/emitter";

const positionLabels = ["1st", "2nd", "3rd", "4th"];

function ResultItem({
  player_name,
  new_score,
  score_change,
  new_position,
}: {
  player_name: string;
  new_score: number;
  score_change: number;
  new_position: number;
}) {
  return (
    <div class={`results_player_score new_position_${new_position}`}>
      <span class="position">{positionLabels[new_position]}</span>
      <span class="player">{player_name}</span>
      <span class="old_score">{new_score - score_change}</span>
      <span class="score_change">{`${score_change >= 0 ? "+" : ""}${score_change}`}</span>
      <span class="new_score">{new_score}</span>
    </div>
  );
}

export function Results({
  info,
  closeResults,
}: {
  info: AllInfo;
  closeResults: () => void;
}) {
  const emit = useContext(Emitter);
  const player_scores = info.game_info.player_scores;
  const score_diffs =
    info.scoring_info?.player_scores ?? Array(info.player_count).fill(0);
  const player_scores_sort = [...player_scores.keys()].sort(
    (a, b) => player_scores[b] - player_scores[a],
  );
  const player_score_elements = [];
  for (let player_index = 0; player_index < info.player_count; ++player_index) {
    player_score_elements.push(
      <ResultItem
        player_name={info.game_info.player_names[player_index]}
        new_score={player_scores[player_index]}
        score_change={score_diffs[player_index]}
        new_position={player_scores_sort.indexOf(player_index)}
      />,
    );
  }
  const onClick = (e: Event) => {
    e.preventDefault();
    closeResults();
    emit("next_round");
  };
  return (
    <div id="results">
      <div id="scores_header">Scores</div>
      <div id="results_player_scores">{player_score_elements}</div>
      <button type="button" id="next_round" onClick={onClick}>
        {info.is_game_end ? "End game" : "Start next round"}
      </button>
    </div>
  );
}
