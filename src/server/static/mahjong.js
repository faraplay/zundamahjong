
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

const set_player_form = document.getElementById('set_player_form');
const set_player_select = document.getElementById('set_player_select');
const history_list = document.getElementById('history_list');

set_player_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (set_player_select.value) {
        socket.emit('set_player', set_player_select.value);
    }
});

socket.on('list_all', (history) => {
    console.log(history);
    for (const playeraction of history) {
        console.log(playeraction)
        const player = playeraction["player"];
        const action = playeraction["action"];
        const action_type = action_types[action["action_type"]];
        const tile = action["tile"];
        const item = document.createElement('li');
        item.textContent = `Player: ${player}, Action: ${action_type}` + 
        (tile != 0 ? `, Tile: ${tile}` : "");
        history_list.appendChild(item);
    }
});