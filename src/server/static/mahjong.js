
const socket = io();

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

const player_indicator = document.getElementById('player_indicator');
const history_list = document.getElementById('history_list');
const discard_pool = document.getElementById('discard_pool');
const calls_list = document.getElementById('calls_list');
const hand_div = document.getElementById('hand');
const actions_div = document.getElementById('actions');

set_player_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (set_player_select.value) {
        socket.emit('set_player', set_player_select.value);
    }
});

function createTileElement(tile) {
    const item = document.createElement('img');
    item.src = tile_images[tile];
    item.alt = tile;
    return item;
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
    const call_item = document.createElement("div");
    const call_type_item = document.createElement("span");
    call_type_item.textContent = call_types[call.call_type];
    call_item.replaceChildren(
        call_type_item,
        ...call.tiles.map(createTileElement)
    )
    return call_item
}

function createPlayerCallsElement(player_calls) {
    const player_item = document.createElement('li');
    const player_item_title = document.createElement('b');
    player_item_title.textContent = `Player ${player_calls.player}`;
    player_item.replaceChildren(
        player_item_title,
        ...player_calls.calls.map(createCallElement)
    );
    return player_item;
}

function createActionElement(action) {
    const action_item = document.createElement('button');
    const action_text = action_types[action.action_type];
    action_item.textContent = action_text;
    if (action.tile != 0) {
        action_item.appendChild(createTileElement(action.tile))
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

socket.on('all_info', (info) => {
    console.log(info);
    player_indicator.textContent = `You are Player ${info.player}`;
    history_list.replaceChildren(...info.history.map(createHistoryEntryElement));
    discard_pool.replaceChildren(...info.discards.map(createTileElement));
    calls_list.replaceChildren(...info.player_calls.map(createPlayerCallsElement));
    hand_div.replaceChildren(...info.hand.map(createTileElement));
    actions_div.replaceChildren(...info.actions.map(createActionElement));
});