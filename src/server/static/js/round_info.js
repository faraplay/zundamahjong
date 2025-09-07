const round_info_div = document.getElementById('round_info');
const seat_indicator = document.getElementById('seat_indicator');
const tiles_left_indicator = document.getElementById('tiles_left');
const history_list = document.getElementById('history_list');

function setRoundInfo(round_info) {
    seat_indicator.textContent = `You are Player ${round_info.seat}`;
    tiles_left_indicator.textContent = `${round_info.tiles_left} tiles left`;
    history_list.replaceChildren(...round_info.history.map(createHistoryEntryElement));

    setDiscards(round_info.seat, round_info.discards);
    setCalls(round_info.seat, round_info.calls);
    setHand(round_info.hand);

    if (round_info.discards.length > 0) {
        last_discard = round_info.discards.at(-1).tile;
    } else {
        last_discard = 0
    }
    setActions(round_info.actions, last_discard);
}
