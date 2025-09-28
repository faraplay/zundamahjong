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
    <button type="button" id="see_results" onClick={onSeeResultsClick}>
      Next
    </button>
  );
  if (!scoring_info) {
    return (
      <div id="win_totals">
        <div id="win_player">The round is a draw...</div>
        {seeResultsButton}
      </div>
    );
  }
  return (
    <div id="win_totals">
      <div id="win_player">{`${win_player_name} wins!`}</div>
      <div id="total_han">{`${scoring_info.han_total} han`}</div>
      <div id="tsumo_or_ron">
        {scoring_info.lose_player == null ? "Tsumo" : "Ron"}
      </div>
      <div id="total_score">
        {scoring_info.player_scores[scoring_info.win_player]}
      </div>
      {seeResultsButton}
    </div>
  );
}
