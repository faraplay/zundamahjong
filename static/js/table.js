const table_hand_elements = [0, 1, 2, 3].map(
    player => document.querySelector(`.table_hand_outer.player_${player} .table_hand`)
);
const player_discards_elements = [0, 1, 2, 3].map(
    player => document.querySelector(`.player_discards.player_${player}`)
);
const player_calls_elements = [0, 1, 2, 3].map(
    player => document.querySelector(`.player_calls.player_${player}`)
);
const player_flowers_elements = [0, 1, 2, 3].map(
    player => document.querySelector(`.player_flowers.player_${player}`)
);

function createTableTileElement(tile) {
    const tile_element = createTileElement(tile);
    tile_element.firstChild.classList.add('tile_face');
    tile_element.firstChild.classList.add('tile_front');
    for (const class_name of ['tile_back', 'tile_left', 'tile_right', 'tile_top', 'tile_bottom']) {
        const side_item = document.createElement('span');
        side_item.classList.add('tile_face');
        side_item.classList.add(class_name);
        tile_element.appendChild(side_item);
    }
    tile_element.appendChild(tile_element.firstChild);
    return tile_element;
}

function setTableHands(info) {
    const known_hands = Array(info.player_count);
    known_hands[info.player_index] = info.round_info.hand;
    if (info.win_info?.win) {
        known_hands[info.win_info.win.win_player] = info.win_info.win.hand;
    }
    const hand_counts = info.round_info.hand_counts;
    const win_player = info.win_info?.win?.win_player;
    for (var player = 0; player < info.player_count; ++player) {
        const tiles = known_hands[player] ?? Array(hand_counts[player]).fill(0);
        table_hand_elements[player].replaceChildren(...tiles.map(createTableTileElement));
        if (player == win_player) {
            table_hand_elements[player].classList.add('won_hand');
        } else {
            table_hand_elements[player].classList.remove('won_hand');
        }
    }
}

function setDiscards(discards) {
    for (var player = 0; player < player_count; ++player) {
        const player_discard_tiles =
            discards.filter(discard => discard.player == player)
                .map(discard => discard.tile);
        player_discards_elements[player].replaceChildren(
            ...player_discard_tiles.map(createTableTileElement)
        )
    }
}

function createTableCallElement(call) {
    const call_element = document.createElement("span");
    call_element.classList.add('call');
    call_element.replaceChildren(
        ...call.tiles.map(createTableTileElement)
    )
    return call_element;
}

function setCalls(calls) {
    for (var player = 0; player < player_count; ++player) {
        player_calls_elements[player].replaceChildren(
            ...calls[player].map(createTableCallElement)
        )
    }
}

function setFlowers(flowers) {
    for (var player = 0; player < player_count; ++player) {
        player_flowers_elements[player].replaceChildren(
            ...flowers[player].map(createTableTileElement)
        )
    }
}
