const round_info_div = document.getElementById('round_info');
const player_indicator = document.getElementById('player_indicator');

const wind_sub_round_element = document.getElementById('wind_sub_round');
const tiles_left_indicator = document.getElementById('tiles_left');
const player_wind_indicator_elements = [0, 1, 2, 3].map(
    player => document.querySelector(`.player_indicator.player_${player}`)
)
const score_elements = [0, 1, 2, 3].map(
    player => document.querySelector(`.score.player_${player}`)
);

const history_list = document.getElementById('history_list');

const player_winds = ['東', '南', '西', '北']

function setPlayerWindIndicators(sub_round) {
    for (var player = 0; player < player_count; ++player) {
        player_wind_indicator_elements[player].textContent =
            player_winds[(player - sub_round + player_count) % player_count];
    }
}

function setScores(scores) {
    for (var player = 0; player < player_count; ++player) {
        score_elements[player].textContent = `${scores[player]}`;
    }
}

function setRoundInfo(round_info, win) {
    const round_status = round_statuses[round_info.status];
    round_info_div.classList.remove(...round_info_div.classList);
    round_info_div.classList.add(`me_player_${round_info.player}`);
    round_info_div.classList.add(`status_${round_status}`)

    player_indicator.textContent = `You are Player ${round_info.player}`;
    wind_sub_round_element.textContent =
        `${player_winds[round_info.wind_round]}${round_info.sub_round + 1}-${round_info.draw_count}`;
    tiles_left_indicator.textContent = round_info.tiles_left;
    setPlayerWindIndicators(round_info.sub_round)
    setScores(round_info.player_scores)

    history_list.replaceChildren(...round_info.history.map(createHistoryEntryElement));

    const known_hands = Array(player_count);
    known_hands[round_info.player] = round_info.hand;
    if (win) {
        known_hands[win.win_player] = win.hand;
    }
    setTableHands(known_hands, round_info.hand_counts, win?.win_player);

    setDiscards(round_info.discards);
    setCalls(round_info.calls);
    setFlowers(round_info.flowers);

    if (round_status == "END") {
        setHand([]);
        setActions([], 0)
    } else {
        setHand(round_info.hand);
        if (!(round_info.current_player == round_info.player
            && (round_status == "PLAY"
                || round_status == "CALLED_PLAY")
        )) {
            disableHandDiscards();
        }
        if (round_info.discards.length > 0) {
            last_discard = round_info.discards.at(-1).tile;
        } else {
            last_discard = 0
        }
        setActions(round_info.actions, last_discard);
    }
}
