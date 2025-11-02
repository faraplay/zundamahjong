import type { Scoring } from "../../../types/game";

import "./win_total_score.css";

export function WinTotalScore({
  win_player_name,
  scoring_info,
  goToResults,
}: {
  win_player_name: string;
  scoring_info: Scoring | null;
  goToResults: () => void;
}) {
  const onSeeResultsClick = (e: Event) => {
    e.preventDefault();
    goToResults();
  };
  const seeResultsButton = (
    <button type="button" class="see_results" onClick={onSeeResultsClick}>
      Next
    </button>
  );
  if (!scoring_info) {
    return (
      <div class="win_totals">
        <div class="win_player">The round is a draw...</div>
        {seeResultsButton}
      </div>
    );
  }
  return (
    <div class="win_totals">
      <div class="win_player">{`${win_player_name} wins!`}</div>
      <div class="scoring_values">{`${scoring_info.han} han, ${scoring_info.fu} fu`}</div>
      <div class="tsumo_or_ron">
        {scoring_info.lose_player == null ? "Tsumo" : "Ron"}
      </div>
      <div class="total_score">
        {scoring_info.player_scores[scoring_info.win_player]}
      </div>
      {seeResultsButton}
    </div>
  );
}
