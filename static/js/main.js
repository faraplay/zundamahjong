var player_count = 4;

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
    setRoundInfo(info.round_info, info.win_info?.win);
    if (round_info.action_selected) {
        disableActions();
    }
    setWinInfo(info.round_info.player_scores, info.win_info);
})
