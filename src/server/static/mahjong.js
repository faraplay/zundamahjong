
const socket = io();

const ACTION_NOTHING = 0;
const ACTION_DRAW = 1;
const ACTION_DISCARD = 2;
const ACTION_CHI_A = 3;
const ACTION_CHI_B = 4;
const ACTION_CHI_C = 5;
const ACTION_PON = 6;
const ACTION_OPEN_KAN = 7;
const ACTION_ADD_KAN = 8;
const ACTION_CLOSED_KAN = 9;
const ACTION_FLOWER = 10;
const ACTION_RON = 11;
const ACTION_TSUMO = 12;

const action_types = [
    "NOTHING",
    "DRAW",
    "DISCARD",
    "CHI_A",
    "CHI_B",
    "CHI_C",
    "PON",
    "OPEN_KAN",
    "ADD_KAN",
    "CLOSED_KAN",
    "FLOWER",
    "RON",
    "TSUMO"
];

const call_types = [
    "PAIR",
    "CHI",
    "PON",
    "OPEN_KAN",
    "ADD_KAN",
    "CLOSED_KAN",
    "FLOWER",
    "THIRTEEN_ORPHANS",
];

const tile_images = {
    1: "mahjongtiles/character/01.svg",
    2: "mahjongtiles/character/02.svg",
    3: "mahjongtiles/character/03.svg",
    4: "mahjongtiles/character/04.svg",
    5: "mahjongtiles/character/05.svg",
    6: "mahjongtiles/character/06.svg",
    7: "mahjongtiles/character/07.svg",
    8: "mahjongtiles/character/08.svg",
    9: "mahjongtiles/character/09.svg",
    11: "mahjongtiles/dot/01.svg",
    12: "mahjongtiles/dot/02.svg",
    13: "mahjongtiles/dot/03.svg",
    14: "mahjongtiles/dot/04.svg",
    15: "mahjongtiles/dot/05.svg",
    16: "mahjongtiles/dot/06.svg",
    17: "mahjongtiles/dot/07.svg",
    18: "mahjongtiles/dot/08.svg",
    19: "mahjongtiles/dot/09.svg",
    21: "mahjongtiles/bamboo/01.svg",
    22: "mahjongtiles/bamboo/02-01.svg",
    23: "mahjongtiles/bamboo/03-01.svg",
    24: "mahjongtiles/bamboo/04-01.svg",
    25: "mahjongtiles/bamboo/05-01.svg",
    26: "mahjongtiles/bamboo/06-01.svg",
    27: "mahjongtiles/bamboo/07-01.svg",
    28: "mahjongtiles/bamboo/08-01.svg",
    29: "mahjongtiles/bamboo/09-01.svg",
    31: "mahjongtiles/wind/01.svg",
    32: "mahjongtiles/wind/02.svg",
    33: "mahjongtiles/wind/03.svg",
    34: "mahjongtiles/wind/04.svg",
    35: "mahjongtiles/dragon/03.svg",
    36: "mahjongtiles/dragon/02.svg",
    37: "mahjongtiles/dragon/01.svg",
    41: "mahjongtiles/season/01.svg",
    42: "mahjongtiles/season/02.svg",
    43: "mahjongtiles/season/03.svg",
    44: "mahjongtiles/season/04.svg",
    45: "mahjongtiles/flower/01.svg",
    46: "mahjongtiles/flower/02.svg",
    47: "mahjongtiles/flower/03.svg",
    48: "mahjongtiles/flower/04.svg",
}

const set_player_form = document.getElementById('set_player_form');
const set_player_select = document.getElementById('set_player_select');

const game_info_div = document.getElementById('game_info');
const player_indicator = document.getElementById('player_indicator');
const tiles_left_indicator = document.getElementById('tiles_left');
const history_list = document.getElementById('history_list');
const discard_pool = document.getElementById('discard_pool');
const calls_list = document.getElementById('calls_list');
const hand_div = document.getElementById('hand');
const actions_div = document.getElementById('actions');

const win_info_div = document.getElementById('win_info');
const win_player_indicator = document.getElementById('win_player');
const win_hand_div = document.getElementById('win_hand');
const win_calls_div = document.getElementById('win_calls');
const new_game_button = document.getElementById('new_game');

set_player_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (set_player_select.value) {
        socket.emit('set_player', set_player_select.value);
    }
});

new_game_button.addEventListener('click', (e) => {
    e.preventDefault();
    console.log("startinng new game");
    socket.emit('new_game');
})

function createTileImageElement(tile) {
    const item = document.createElement('img');
    item.classList.add('tile');
    item.src = tile_images[tile];
    item.alt = tile;
    return item;
}

function createTileElement(tile) {
    const item = document.createElement('div');
    item.classList.add('tile_div');
    item.appendChild(createTileImageElement(tile));
    return item;
}

function createTableTileElement(tile) {
    const item = createTileElement(tile);
    item.firstChild.classList.add('tile_face');
    for (const class_name of ['tile_left', 'tile_right', 'tile_top', 'tile_bottom']) {
        const side_item = document.createElement('div');
        side_item.classList.add('tile_face');
        side_item.classList.add('tile_side');
        side_item.classList.add(class_name);
        item.appendChild(side_item);
    }
    item.appendChild(item.firstChild)
    return item;
}

function createHandTileElement(tile) {
    const button = document.createElement('button');
    button.classList.add('hand_tile_button');
    button.appendChild(createTileElement(tile));
    button.addEventListener('click', (e) => {
        e.preventDefault();
        socket.emit('action', {
            'action_type': ACTION_DISCARD,
            'tile': tile
        })
    });
    return button;
}

function createHistoryEntryElement(history_entry) {
    const action = history_entry.action;
    const action_type = action_types[action.action_type];
    const history_item = document.createElement('li');
    const history_text_item = document.createElement('span');
    history_text_item.textContent =
        `Player: ${history_entry.player}, Action: ${action_type}`;
    history_item.appendChild(history_text_item);
    if (action.tile != 0) {
        history_item.appendChild(createTileElement(action.tile))
    }
    return history_item;
}

function createCallElement(call) {
    const call_item = document.createElement("span");
    call_item.classList.add('call');
    const call_type_item = document.createElement("h4");
    call_type_item.textContent = call_types[call.call_type];
    call_item.replaceChildren(
        call_type_item,
        ...call.tiles.map(createTileElement)
    )
    return call_item
}

function createCallElementIndexed(call, startIndex) {
    const call_item = document.createElement("span");
    call_item.classList.add('call');
    const call_type_item = document.createElement("h4");
    call_type_item.textContent = call_types[call.call_type];
    call_item.appendChild(call_type_item);
    var index = startIndex + call.tiles.length - 1;
    for (const tile of call.tiles) {
        tile_item = createTableTileElement(tile);
        tile_item.style.setProperty('--player-calls-tile-x-index', index);
        --index;
        call_item.appendChild(tile_item)
    }
    return call_item
}

function createPlayerCallsElement(player_calls) {
    const player_item = document.createElement('div');
    player_item.classList.add('player_calls');
    const player_item_title = document.createElement('h4');
    player_item_title.textContent = `Player ${player_calls.player}`;
    player_item.appendChild(player_item_title);

    var index = 0;
    for (const call of player_calls.calls) {
        call_item = createCallElementIndexed(call, index);
        player_item.appendChild(call_item);
        index += call.tiles.length;
    }
    return player_item;
}

function createActionElement(action, last_discard) {
    const action_item = document.createElement('button');
    const action_text = action_types[action.action_type];
    action_item.textContent = action_text;
    
    switch (action.action_type) {
        case ACTION_CHI_A:
            for (const tile of [last_discard, last_discard+1, last_discard+2]) {
                action_item.appendChild(createTileElement(tile))
            }
            break;
        case ACTION_CHI_B:
            for (const tile of [last_discard-1, last_discard, last_discard+1]) {
                action_item.appendChild(createTileElement(tile))
            }
            break;
        case ACTION_CHI_C:
            for (const tile of [last_discard-2, last_discard-1, last_discard]) {
                action_item.appendChild(createTileElement(tile))
            }
            break;
        case ACTION_PON:
            for (const tile of [last_discard, last_discard, last_discard]) {
                action_item.appendChild(createTileElement(tile))
            }
            break;
        case ACTION_OPEN_KAN:
            for (const tile of [last_discard, last_discard, last_discard, last_discard]) {
                action_item.appendChild(createTileElement(tile))
            }
            break;
        case ACTION_ADD_KAN:
        case ACTION_CLOSED_KAN:
        case ACTION_FLOWER:
            action_item.appendChild(createTileElement(action.tile))
            break;
    }
    action_item.addEventListener('click',
        (e) => {
            e.preventDefault();
            console.log("sending action", action)
            socket.emit('action', action)
        }
    )
    return action_item;
}

function disableHandDiscards() {
    for (const button of hand_div.children) {
        button.disabled = true;
    }
}

function disableActions() {
    for (const button of actions_div.children) {
        button.disabled = true;
    }
    disableHandDiscards()
}

socket.on('game_info', (info) => {
    console.log(info);
    game_info_div.hidden = false;
    win_info_div.hidden = true;
    player_indicator.textContent = `You are Player ${info.player}`;
    tiles_left_indicator.textContent = `${info.tiles_left} tiles left`;
    history_list.replaceChildren(...info.history.map(createHistoryEntryElement));

    discard_items = info.discards.map(createTableTileElement);
    for (var i=0; i<info.discards.length; ++i) {
        const item = discard_items[i];
        item.style.setProperty('--discard-tile-x-index', i % 15);
        item.style.setProperty('--discard-tile-y-index', Math.floor(i / 15));
    }
    discard_pool.replaceChildren(...discard_items);

    player_calls = info.player_calls.map(createPlayerCallsElement);
    for (var i=0; i<4; ++i) {
        player_calls[(info.player + i) % 4].classList.add('player_calls');
        player_calls[(info.player + i) % 4].classList.add(`position_${i}`);
    }
    calls_list.replaceChildren(...player_calls);

    hand_div.replaceChildren(...info.hand.map(createHandTileElement));
    last_discard = info.discards.at(-1);
    actions_div.replaceChildren(...info.actions.filter((action) => {
        return action.action_type != ACTION_DISCARD
    }).map((action) => {
        return createActionElement(action, last_discard)
    }));
    if (info.actions.every((action) => {return action.action_type != ACTION_DISCARD})) {
        disableHandDiscards();
    }
    if (info.action_selected) {
        disableActions();
    }
});

socket.on('win_info', (info) => {
    console.log(info);
    game_info_div.hidden = true;
    win_info_div.hidden = false;
    if (info) {
        win_player_indicator.textContent = `Player ${info.win_player} wins!`;
        win_hand_div.replaceChildren(...info.hand.map(createTileElement));
        win_calls_div.replaceChildren(...info.calls.map(createCallElement));
    } else {
        win_player_indicator.textContent = "The game is a draw..."
    }
})

socket.on('action_received', () => {
    console.log("action received");
    disableActions();
})