
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

const action_supertypes = [
    7,
    7,
    0,
    1,
    1,
    1,
    2,
    3,
    3,
    3,
    4,
    5,
    6
];

const action_supertype_strings = [
    "",
    "Chii",
    "Pon",
    "Kan",
    "Flower",
    "Ron",
    "Tsumo",
    "Pass"
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

set_player_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (set_player_select.value) {
        socket.emit('set_player', set_player_select.value);
    }
});

function createTileImageElement(tile) {
    const item = document.createElement('img');
    item.classList.add('tile');
    item.src = tile_images[tile];
    item.alt = tile;
    item.width = 60;
    item.height = 80;
    return item;
}

function createTileElement(tile) {
    const item = document.createElement('span');
    item.classList.add('tile_div');
    item.appendChild(createTileImageElement(tile));
    return item;
}


function createStraightTileElement(tile) {
    const tile_item = createTileElement(tile);
    const tile_back_item = document.createElement('div');
    tile_back_item.classList.add('tile_back_layer');
    tile_item.appendChild(tile_back_item);
    const tile_middle_item = document.createElement('div');
    tile_middle_item.classList.add('tile_middle_layer');
    tile_item.appendChild(tile_middle_item);
    tile_item.appendChild(tile_item.firstChild);
    return tile_item;
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
