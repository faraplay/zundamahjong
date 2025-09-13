var player_count = 4;

const round_info_div = document.getElementById('round_info');

function disableActions() {
    for (const button of actions_div.children) {
        button.disabled = true;
    }
    disableHandDiscards()
}

socket.on('info', (info) => {
    console.log(info);
    if (round_statuses[info.round_info.status] == "END") {
        win_info_div.hidden = false;
    } else {
        win_info_div.hidden = true;
    }
    results_div.hidden = true;

    player_count = info.player_count;

    round_info_div.classList.remove(...round_info_div.classList);
    round_info_div.classList.add(`me_player_${info.player_index}`);

    setGameInfo(info.game_info);
    setRoundInfo(info.round_info);
    setPlayerInfo(info.player_info);

    setWinInfo(info.win_info);
    setScoringInfo(info.scoring_info);

    const score_diffs = info.scoring_info?.player_scores ?? Array(player_count).fill(0);
    setResults(info.game_info.player_names, info.game_info.player_scores, score_diffs);
    next_round_button.textContent = info.is_game_end ? "End game" : "Start next round";

    setTableHands(info);

    showScreen("game_screen");
})
