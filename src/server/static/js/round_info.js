var player_count = 4

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

function setRoundInfo(round_info) {
    player_count = round_info.player_count;
    round_info_div.className = `me_player_${round_info.player}`;
    player_indicator.textContent = `You are Player ${round_info.player}`;
    wind_sub_round_element.textContent = `${player_winds[round_info.wind_round]}${round_info.sub_round + 1}`
    tiles_left_indicator.textContent = round_info.tiles_left;
    setPlayerWindIndicators(round_info.sub_round)
    setScores(round_info.player_scores)

    history_list.replaceChildren(...round_info.history.map(createHistoryEntryElement));

    setDiscards(round_info.discards);
    setCalls(round_info.calls);

    if (round_info.status == round_status.END) {
        setHand([]);
        setActions([], 0)
    } else {
        setHand(round_info.hand);
        if (round_info.discards.length > 0) {
            last_discard = round_info.discards.at(-1).tile;
        } else {
            last_discard = 0
        }
        setActions(round_info.actions, last_discard);
    }
}
