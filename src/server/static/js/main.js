function disableActions() {
    for (const button of actions_div.children) {
        button.disabled = true;
    }
    disableHandDiscards()
}

socket.on('round_info', (round_info) => {
    console.log(round_info);
    round_info_div.hidden = false;
    win_info_div.hidden = true;
    setRoundInfo(round_info)
    if (round_info.action_selected) {
        disableActions();
    }
});

socket.on('win_info', (win_info) => {
    console.log(win_info);
    round_info_div.hidden = true;
    win_info_div.hidden = false;
    setWinInfo(win_info);
})

socket.on('action_received', () => {
    disableActions();
})
