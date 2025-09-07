const round_info_div = document.getElementById('round_info');
const player_indicator = document.getElementById('player_indicator');
const wind_seat_round_element = document.getElementById('wind_seat_round');
const tiles_left_indicator = document.getElementById('tiles_left');
const scores_element = document.getElementById('scores');
const score_elements = [0, 1, 2, 3].map(
    player => document.querySelector(`.score.player_${player}`)
);

const history_list = document.getElementById('history_list');

const seat_winds = ['東', '南', '西', '北']

function setScores(scores) {
    for (var player = 0; player < 4; ++player) {
        score_elements[player].innerHTML = `<h4>Player ${player}</h4>${scores[player]}`;
    }
}

function setRoundInfo(round_info) {
    round_info_div.className = `me_player_${round_info.player}`;
    player_indicator.textContent = `You are Player ${round_info.player}`;
    wind_seat_round_element.textContent = `${seat_winds[round_info.wind_round]}${round_info.seat_round + 1}`
    tiles_left_indicator.textContent = round_info.tiles_left;
    setScores(round_info.player_scores)

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
