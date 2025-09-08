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

socket.on('win_info', (info) => {
    console.log(info);
    round_info_div.hidden = true;
    win_info_div.hidden = false;
    if (info) {
        win_player_indicator.textContent = `Player ${info.win_player} wins!`;
        win_hand_div.replaceChildren(...info.hand.map(createTileElement));
        win_calls_div.replaceChildren(...info.calls.map(createCallElement));
    } else {
        win_player_indicator.textContent = "The round is a draw..."
    }
})

socket.on('action_received', () => {
    disableActions();
})
