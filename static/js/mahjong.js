
const socket = io();

const ACTION_PASS = 0;
const ACTION_CONTINUE = 1;
const ACTION_DRAW = 2;
const ACTION_DISCARD = 3;
const ACTION_CHI_A = 4;
const ACTION_CHI_B = 5;
const ACTION_CHI_C = 6;
const ACTION_PON = 7;
const ACTION_OPEN_KAN = 8;
const ACTION_ADD_KAN = 9;
const ACTION_CLOSED_KAN = 10;
const ACTION_FLOWER = 11;
const ACTION_RON = 12;
const ACTION_TSUMO = 13;

const action_types = [
    "PASS",
    "CONTINUE",
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
    "THIRTEEN_ORPHANS",
];

const round_statuses = [
    "START",
    "PLAY",
    "CALLED_PLAY",
    "ADD_KAN_AFTER",
    "CLOSED_KAN_AFTER",
    "DISCARDED",
    "LAST_DISCARDED",
    "END",
]

function createTileImageElement(tile) {
    if (tile) {
        const item = document.createElement('img');
        item.classList.add('tile');
        item.src = tile_images[tile];
        item.alt = tile;
        item.width = 60;
        item.height = 80;
        return item;
    }
    else {
        const element = document.createElement('div');
        element.classList.add('tile');
        return element;
    }
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
