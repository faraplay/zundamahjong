function disableActions() {
    for (const button of actions_div.children) {
        button.disabled = true;
    }
    disableHandDiscards()
}

socket.on('info', (info) => {
    console.log(info);
    if (info.round_info.status == round_status.END) {
        win_info_div.hidden = false;
    } else {
        win_info_div.hidden = true;
    }
    results_div.hidden = true;
    setRoundInfo(info.round_info);
    if (round_info.action_selected) {
        disableActions();
    }
    setWinInfo(info.round_info.player_scores, info.win_info);
})

socket.on('action_received', () => {
    disableActions();
})
