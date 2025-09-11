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

function setGameInfo(game_info) {
    wind_sub_round_element.textContent =
        `${player_winds[game_info.wind_round]}${game_info.sub_round + 1}-${game_info.draw_count}`;
    setPlayerWindIndicators(game_info.sub_round)
    setScores(game_info.player_scores)
}

function setRoundInfo(round_info) {
    tiles_left_indicator.textContent = round_info.tiles_left;
    round_info_div.classList.add(`status_${round_info.status}`)

    setDiscards(round_info.discards);
    setCalls(round_info.calls);
    setFlowers(round_info.flowers);

    history_list.replaceChildren(...round_info.history.map(createHistoryEntryElement));
}

function setPlayerInfo(player_info) {
    const can_discard = player_info.actions.some(action => action.action_type == 2);
    const last_tile = player_info.last_tile

    setHand(player_info.hand);
    if (!can_discard) {
        disableHandDiscards();
    }
    setActions(player_info.actions, last_tile);
    if (player_info.action_selected) {
        disableActions();
    }
}
