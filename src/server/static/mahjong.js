
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

const set_player_form = document.getElementById('set_player_form');
const set_player_select = document.getElementById('set_player_select');

const player_indicator = document.getElementById('player_indicator');
const history_list = document.getElementById('history_list');
const discard_pool = document.getElementById('discard_pool');
const calls_list = document.getElementById('calls_list');
const hand_div = document.getElementById('hand');

set_player_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (set_player_select.value) {
        socket.emit('set_player', set_player_select.value);
    }
});

function createTileElement(tile) {
    const item = document.createElement('span');
    item.textContent = tile;
    return item;
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

socket.on('all_info', (info) => {
    console.log(info);
    player_indicator.textContent = `You are Player ${info.player}`;
    history_list.replaceChildren(...info.history.map(
        (playeraction) => {
            const player = playeraction.player;
            const action = playeraction.action;
            const action_type = action_types[action.action_type];
            const tile = action.tile;
            const item = document.createElement('li');
            item.textContent = `Player: ${player}, Action: ${action_type}` + 
                (tile != 0 ? `, Tile: ${tile}` : "");
            return item;
        }
    ));
    discard_pool.replaceChildren(...info.discards.map(createTileElement))
    calls_list.replaceChildren(...info.player_calls.map(createPlayerCallsElement))
    hand_div.replaceChildren(...info.hand.map(createTileElement))
});