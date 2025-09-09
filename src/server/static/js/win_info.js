
const win_info_div = document.getElementById('win_info');
const win_hand_div = document.getElementById('win_hand');
const win_tiles_div = document.getElementById('win_tiles');
const win_calls_div = document.getElementById('win_calls');
const win_flowers_div = document.getElementById('win_flowers');
const yakus_element = document.getElementById('yakus');

const win_player_indicator = document.getElementById('win_player');
const total_han_element = document.getElementById('total_han');
const tsumo_or_ron_element = document.getElementById('tsumo_or_ron');
const total_score_element = document.getElementById('total_score');
const see_results_button = document.getElementById('see_results');

const results_div = document.getElementById('results');
const player_scores_div = document.getElementById('results_player_scores');
const next_round_button = document.getElementById('next_round');

see_results_button.addEventListener('click', (e) => {
    e.preventDefault();
    win_info_div.hidden = true;
    results_div.hidden = false;
});

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

const position_labels = ['1st', '2nd', '3rd', '4th'];

function createPlayerScoreElement(
    player, new_score, score_change, new_position
) {
    const player_score_element = document.createElement('div');
    player_score_element.classList.add('results_player_score');
    player_score_element.classList.add(`new_position_${new_position}`);

    const position_element = document.createElement('span');
    position_element.classList.add('position');
    position_element.textContent = position_labels[new_position];
    player_score_element.appendChild(position_element);

    const player_element = document.createElement('span');
    player_element.classList.add('player');
    player_element.textContent = `Player ${player}`;
    player_score_element.appendChild(player_element);

    const old_score_element = document.createElement('span');
    old_score_element.classList.add('old_score');
    old_score_element.textContent = `${new_score - score_change}`;
    player_score_element.appendChild(old_score_element);

    const score_change_element = document.createElement('span');
    score_change_element.classList.add('score_change');
    score_change_element.textContent = `${score_change >= 0 ? '+' : ''}${score_change}`;
    player_score_element.appendChild(score_change_element);

    const new_score_element = document.createElement('span');
    new_score_element.classList.add('new_score');
    new_score_element.textContent = new_score;
    player_score_element.appendChild(new_score_element);

    return player_score_element;
}

function setResults(win_info) {
    const player_scores_sort = [...win_info.player_scores.keys()].sort(
        (a, b) => (win_info.player_scores[b] - win_info.player_scores[a])
    );
    player_score_elements = [];
    for (let player = 0; player < player_count; ++player) {
        player_score_elements.push(
            createPlayerScoreElement(
                player,
                win_info.player_scores[player],
                win_info.scoring.player_scores[player],
                player_scores_sort.indexOf(player)
            )
        );
    }
    player_scores_div.replaceChildren(...player_score_elements);
}

function setWinInfo(win_info) {
    if (win_info) {
        win_flowers_div.replaceChildren(...win_info.win.flowers.map(createStraightTileElement));
        win_tiles_div.replaceChildren(...win_info.win.hand.map(createStraightTileElement));
        win_calls_div.replaceChildren(...win_info.win.calls.map(createCallElement));

        const win_hand_width = win_info.win.calls.reduce(
            (partial_sum, call) => partial_sum + call.tiles.length + 0.5,
            win_info.win.hand.length
        );
        console.log(win_hand_width + win_info.win.flowers.length);
        if (win_hand_width + win_info.win.flowers.length >= 21.5) {
            win_flowers_div.classList.add('overlap');
        } else {
            win_flowers_div.classList.remove('overlap');
        }
        yakus_element.replaceChildren(
            ...Object.entries(win_info.scoring.yaku_hans).map(createYakuElement)
        );

        win_player_indicator.textContent = `Player ${win_info.win.win_player} wins!`;
        total_han_element.textContent = `${win_info.scoring.han_total} han`;
        tsumo_or_ron_element.textContent = win_info.win.lose_player ? "Ron" : "Tsumo";
        total_score_element.textContent =
            win_info.scoring.player_scores[win_info.win.win_player];
        setResults(win_info);
    } else {
        win_player_indicator.textContent = "The round is a draw...";
    }
}
