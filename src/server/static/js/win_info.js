
const win_info_div = document.getElementById('win_info');
const win_hand_div = document.getElementById('win_hand');
const win_tiles_div = document.getElementById('win_tiles');
const win_calls_div = document.getElementById('win_calls');
const yakus_element = document.getElementById('yakus');

const win_player_indicator = document.getElementById('win_player');
const total_han_element = document.getElementById('total_han');
const total_score_element = document.getElementById('total_score');

const next_round_button = document.getElementById('next_round');

next_round_button.addEventListener('click', (e) => {
    e.preventDefault();
    socket.emit('next_round');
})

function createCallElement(call) {
    const call_item = document.createElement("span");
    call_item.classList.add('call');
    const call_type_item = document.createElement("h4");
    call_type_item.textContent = call_types[call.call_type];
    call_item.replaceChildren(
        call_type_item,
        ...call.tiles.map(createStraightTileElement)
    )
    return call_item
}

function createYakuElement(yakuhan) {
    const [yaku, han] = yakuhan;
    const yaku_element = document.createElement('div');
    yaku_element.classList.add('yaku');
    const yaku_name_element = document.createElement('span');
    yaku_name_element.classList.add('yaku_name');
    yaku_name_element.textContent = yaku;
    yaku_element.appendChild(yaku_name_element);
    const yaku_han_element = document.createElement('span');
    yaku_han_element.classList.add('yaku_han');
    yaku_han_element.textContent = han;
    yaku_element.appendChild(yaku_han_element);
    return yaku_element;
}

function setWinInfo(win_info) {
    if (win_info.win) {
        win_tiles_div.replaceChildren(...win_info.win.hand.map(createStraightTileElement));
        win_calls_div.replaceChildren(...win_info.win.calls.map(createCallElement));
        yakus_element.replaceChildren(
            ...Object.entries(win_info.scoring.yaku_hans).map(createYakuElement)
        );

        win_player_indicator.textContent = `Player ${win_info.win.win_player} wins!`;
        total_han_element.textContent = `${win_info.scoring.han_total} han`;
        total_score_element.textContent =
            win_info.scoring.player_scores[win_info.win.win_player];
    } else {
        win_player_indicator.textContent = "The round is a draw...";
    }
}