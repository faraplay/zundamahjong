const round_info_div = document.getElementById('round_info');
const seat_indicator = document.getElementById('seat_indicator');
const wind_seat_round_element = document.getElementById('wind_seat_round');
const tiles_left_indicator = document.getElementById('tiles_left');
const scores_element = document.getElementById('scores');

const history_list = document.getElementById('history_list');

const seat_winds = ['東', '南', '西', '北']

function setScores(my_seat, scores) {
    scores_element.innerHTML =
        `<h3>Scores</h3>
        <div class="score position_${(0 - my_seat + 4) % 4}">
            <h4>Player 0</h4>
            ${scores[0]}
        </div>
        <div class="score position_${(1 - my_seat + 4) % 4}">
            <h4>Player 1</h4>
            ${scores[1]}
        </div>
        <div class="score position_${(2 - my_seat + 4) % 4}">
            <h4>Player 2</h4>
            ${scores[2]}
        </div>
        <div class="score position_${(3 - my_seat + 4) % 4}">
            <h4>Player 3</h4>
            ${scores[3]}
        </div>`
}

function setRoundInfo(round_info) {
    seat_indicator.textContent = `You are Player ${round_info.seat}`;
    wind_seat_round_element.textContent = `${seat_winds[round_info.wind_round]}${round_info.seat_round + 1}`
    tiles_left_indicator.textContent = round_info.tiles_left;
    setScores(round_info.seat, round_info.player_scores)

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
